import os
import pickle
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

import requests
from langchain_community.document_loaders import (ArxivLoader, PDFMinerLoader,
                                                  WikipediaLoader)
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from tqdm import tqdm

ROOT = Path(__file__).parent.parent.parent
LIMIT_PER_SOURCE = 10


class SemanticScholarLoader:
    def __init__(self, query: str, load_max_docs: int = LIMIT_PER_SOURCE) -> None:
        self.query = query
        self.load_max_docs = load_max_docs

        self.pdfs_dir = ROOT / "database/pdfs"
        self.pdfs_dir.mkdir(parents=True, exist_ok=True)

    def load(self):
        papers = self.__get_metadata()
        papers = self.__add_pdf(papers)

        docs = []
        for paper in papers:
            try:
                loader = PDFMinerLoader(paper["pdf_path"])
                data = loader.load()
            except Exception:
                continue

            for d in data:
                d.metadata.update(paper)
                d.metadata["source"] = paper["openAccessPdf"]["url"]
                if paper["abstract"]:
                    d.metadata["summary"] = paper["abstract"]
                else:
                    d.metadata["summary"] = d.page_content[:500]

            docs.extend(data)

        return docs

    def __get_metadata(self) -> List[Dict]:
        endpoint = "https://api.semanticscholar.org/graph/v1/paper/search"
        params = {
            "query": self.query,
            "fields": "title,abstract,year,isOpenAccess,openAccessPdf,citationCount",
            "limit": self.load_max_docs,
            "openAccessPdf": "",
        }
        headers = {"x-api-key": os.getenv("PAPERS_SEMANTIC_SCHOLAR")}

        response = requests.get(endpoint, params=params, headers=headers)
        if response.status_code == 200:
            papers = response.json()["data"]
        else:
            print(f"Failed to fetch papers. Status code: {response.status_code}")

        return papers

    def __download_pdf(self, paper: Dict) -> str:
        if paper["isOpenAccess"]:
            safe_title = (
                paper["title"].replace(" ", "_").replace("/", "_").replace("\\", "_")
            )
            file_name = f"{safe_title}_{paper['year']}.pdf"
            file_path = self.pdfs_dir / file_name

            with requests.Session() as session:
                session.headers.update({"User-Agent": "Mozilla/5.0"})
                response = session.get(paper["openAccessPdf"]["url"])

            response.raise_for_status()

            with open(file_path, "wb") as f:
                f.write(response.content)

            return file_path

    def __add_pdf(self, papers: List[Dict]) -> List[str]:
        for paper in papers:
            try:
                pdf_path = self.__download_pdf(paper)
                paper["pdf_path"] = str(pdf_path)
            except Exception:
                paper["pdf_path"] = None

        return papers


class DataCrawler:
    def crawl(self, query: str) -> List[Document]:
        docs = []

        loader_wikipedia = WikipediaLoader(
            query=query,
            load_max_docs=LIMIT_PER_SOURCE,
            doc_content_chars_max=1_000_000,
        )
        loader_arxiv = ArxivLoader(query=query, load_max_docs=LIMIT_PER_SOURCE)
        loader_semantic_scholar = SemanticScholarLoader(
            query=query, load_max_docs=LIMIT_PER_SOURCE
        )

        docs_arxiv = loader_arxiv.load()
        docs_wikipedia = loader_wikipedia.load()
        docs_semantic_scholar = loader_semantic_scholar.load()

        self.__clean_metadata(docs_arxiv, [])

        docs.extend(docs_arxiv)
        docs.extend(docs_wikipedia)
        docs.extend(docs_semantic_scholar)

        return docs

    def __clean_metadata(
        self, docs_arxiv: List[Document], docs_pubmed: List[Document]
    ) -> List[Dict]:
        for d in docs_arxiv:
            d.metadata["title"] = d.metadata.pop("Title")
            d.metadata["summary"] = d.metadata.pop("Summary")
            d.metadata["source"] = f"ARXIV: {d.metadata['title']}"

        for d in docs_pubmed:
            d.metadata["title"] = d.metadata.pop("Title")
            d.metadata["summary"] = d.metadata["title"]
            d.metadata["source"] = f"PUBMED: {d.metadata['uid']}"


class Database:
    def __init__(
        self, name: str, initialize: bool = False, queries: Optional[List[str]] = None
    ) -> None:
        self.path = ROOT / f"database/{name}"
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200, add_start_index=True
        )
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        self.crawler = DataCrawler()

        if initialize:
            if not queries:
                raise ValueError("Queries must be provided for initialization.")

            self.vector: FAISS = self.__initialize(queries)
        else:
            self.vector: FAISS = self.__load()

    def __initialize(self, queries: List[str]) -> FAISS:
        """Only run once to initialize the database."""
        docs = []
        for query in tqdm(queries, desc="Processing keywords", total=len(queries)):
            docs.extend(self.crawler.crawl(query))

        self.__save_pickle(docs)

        splits = self.splitter.split_documents(docs)

        database = FAISS.from_documents(splits, self.embeddings)
        database.save_local(self.path)

        return database

    def __save_pickle(self, docs: List[Document]) -> None:
        now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file = f"{now}.pkl"
        path = Path("database/docs") / file
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "wb") as file:
            pickle.dump(docs, file)

    def __load(self):
        """Used for inference."""
        return FAISS.load_local(
            self.path, self.embeddings, allow_dangerous_deserialization=True
        )

    def extend(self, query: str):
        """Extend the database with new documents."""
        docs = self.crawler.crawl(query)

        splits = self.splitter.split_documents(docs)
        self.vector.add_documents(splits)
