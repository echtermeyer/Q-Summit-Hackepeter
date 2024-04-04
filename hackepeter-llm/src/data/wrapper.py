from typing import List

from langchain_core.documents import Document

from src.data.loader import Database


class KnowledgeBase:
    def __init__(self) -> None:
        self.database = Database(
            name="vector_db",
            initialize=False,
        )

    def query(self, keywords: str, query: str, k: int) -> List[Document]:
        # return list of documents, each document has .page_content and .metadata. Metadata has min. title, summary, source.
        # 1000 characters for content
        # self.database.extend(keywords)

        return self.database.vector.similarity_search(query, k=k)
