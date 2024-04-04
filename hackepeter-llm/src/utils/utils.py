import json
from typing import List
from pathlib import Path
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser

from src.agent.prompts import (description_chain_prompt,
                               evaluation_chain_prompt, keyword_chain_prompt,
                               science_chain_prompt, system_chain_prompt)
from src.data.wrapper import KnowledgeBase

path = Path("src/data/graph.json")


def initialize_graph():
    graph = []
    with open(path, "w") as f:
        json.dump(graph, f)

    return None


def read_graph():
    """
    Read the graph from a file.

    Returns:
        list: The graph.
    """
    with open(path, "r") as f:
        graph = json.load(f)
    return graph


def update_graph(node_path: str):
    """
    Create a new node in the graph based on the given node path.
    The path consists of the node names separated by slashes (e.g. "Transportation/Cars/Speed Limit")
    The first part is the root node, the second part is a section, and the third part is an action.
    The node path must have a depth of 1 to 3.

    Args:
        node_path (str): The path of the node.

    Returns:
        None
    """
    graph = read_graph()

    path_parts = node_path.split("/")
    path_depth = len(path_parts)

    if path_depth == 1:
        id = 1
        parent_id = None
        name = path_parts[0]
        type = "root"
        metadata = generate_metadata(path_parts, type)

    elif path_depth <= 3:
        ids = [node["id"] for node in graph]
        id_name_mapping = {node["name"]: node["id"] for node in graph}

        if not graph:
            return "The graph is empty. You must add a root node first."

        id = max(ids) + 1
        parent_id = id_name_mapping.get(path_parts[-2])
        if not parent_id:
            return "Parent node does not exist. You must specify the area first before adding an action."

        name = path_parts[-1]
        type = "area" if path_depth == 2 else "action"
        previous_content = ""
        for node in graph:
            if node["id"] == parent_id:
                previous_content = node["metadata"]
                break

        if previous_content.get("description"):
            previous_content = previous_content["description"]
        else:
            previous_content = ""

        metadata = generate_metadata(path_parts, type, previous_content)

    else:
        return "Path depth must be between 1 and 3."

    new_node = {
        "id": id,
        "parent_id": parent_id,
        "name": name,
        "type": type,
        "metadata": metadata,
    }

    if new_node not in [node["id"] for node in graph]:
        graph.append(new_node)
    else:
        return "Node already exists in the graph."

    with open(path, "w") as f:
        json.dump(graph, f)

    message = f"Node '{name}' added to the graph."
    return message


def generate_metadata(
    path_parts: List[str],
    type: str,
    previous_description: str = "",
    power: bool = False,
):

    model = "gpt-4-turbo-preview" if power else "gpt-3.5-turbo"
    llm = ChatOpenAI(model_name=model, temperature=0)

    try:
        node_stack = ""
        if len(path_parts) == 3:
            node_stack = (
                path_parts[2]
                + " within the area "
                + path_parts[1]
                + " within the sector "
                + path_parts[0]
            )
        elif len(path_parts) == 2:
            node_stack = path_parts[1] + " within the sector " + path_parts[0]
        else:
            node_stack = path_parts[0]

        prompt = system_chain_prompt.format(type=type, node_stack=node_stack)
        prompt_template = ChatPromptTemplate.from_messages(
            [("system", prompt), ("human", "{input}")]
        )
        chain_component = prompt_template | llm | StrOutputParser()

        prompt = description_chain_prompt.format(
            type=type, previous_description=previous_description
        )

        description = str(chain_component.invoke({"input": f"{prompt}"}))

        if type == "root" or type == "area":
            return {"description": description}

        elif type == "action":
            try:

                prompt = keyword_chain_prompt.format(
                    name=path_parts[-1], current_description=description
                )

                keywords_string = str(chain_component.invoke({"input": f"{prompt}"}))

            except Exception as e:
                print(e)
                return {
                    "description": description,
                    "keywords": f"Could not generate keywords. {e}",
                }

            try:
                knowledge_base = KnowledgeBase()
                docs = knowledge_base.query(
                    keywords=keywords_string, query=description, k=5
                )
                sources = {doc.metadata["title"]: doc.metadata["source"] for doc in docs}
                # docs is a list of documents, each document has .page_content (1000 chars) and .metadata. Metadata has min. title, summary, source.
                joined_docs = " ".join(doc.page_content for doc in docs)

                prompt = science_chain_prompt.format(
                    name=path_parts[-1],
                    docs_content=joined_docs,
                    current_description=description,
                )
                science_string = str(chain_component.invoke({"input": f"{prompt}"}))

            except Exception as e:
                print(e)
                return {
                    "description": description,
                    "keywords": keywords_string,
                    "science": f"Could not generate science. {e}",
                    "sources": f"No science so no sources. {e}",
                }

            try:

                class Evaluation(BaseModel):
                    effectiveness: float = Field(
                        description="The estimated effectiveness of the action in reducing carbon emissions. 1 marking the lowest effectiveness and 5 marking the highest."
                    )
                    scientific_concensus: float = Field(
                        description="The amount of evidence / support for the effectiveness of the action. 1 marking the lowest and 5 marking the highest."
                    )
                    realization_speed: float = Field(
                        description="The estimated time it will take for the action to have an impact on carbon emissions. 1 marking the slowest and 5 marking the fastest."
                    )

                parser = JsonOutputParser(pydantic_object=Evaluation)
                chain_component = prompt_template | llm | parser
                prompt = evaluation_chain_prompt.format(
                    name=path_parts[-1],
                    current_description=description,
                    science=science_string,
                    format_instructions=parser.get_format_instructions(),
                )
                metrics = chain_component.invoke({"input": f"{prompt}"})
            except Exception as e:
                print(e)
                return {
                    "description": description,
                    "keywords": keywords_string,
                    "science": science_string,
                    "sources": sources,
                    "metrics": f"Could not generate metrics. {e}",
                }
            return {
                "description": description,
                "keywords": keywords_string,
                "science": science_string,
                "sources": sources,
                "metrics": metrics,
            }

    except Exception as e:
        print(e)
        return {"description": f"Could not create Metadata. {e}"}
