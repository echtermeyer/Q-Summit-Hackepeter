from langchain.agents import tool
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from src.utils.utils import read_graph, update_graph

# wir geben englische keywords - eric returned referencen (json mit name, content etc)

done = False


@tool
def get_nodes():
    """
    Returns the graph nodes.

    Returns:
        list: A list of dictionaries representing the nodes in the graph.
    """
    graph = read_graph()
    return graph


@tool
def create_node(node_path: str) -> str:
    """
    Create a new node in the graph based on the given node path.
    The path consists of the node names separated by slashes (e.g. "Transportation/Cars/Speed Limit")
    The first part is the root node, the second part is a section, and the third part is an action.
    The node path must have a depth of 1 to 3.

    Args:
        node_path (str): The path of the node.

    Returns:
        str
    """
    message = update_graph(node_path)
    return message
