import json
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from typing import List

from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel

from src.agent.agent import Agent
from src.agent.chatbot import ActionChatbot, ChatInput
from src.agent.tools import create_node, get_nodes
from src.utils.utils import read_graph

router = APIRouter()

ROOT = Path(__file__).parent.parent.parent
with open(ROOT / "src/data/demo_api.json", "r") as f:
    DEMO_DATA = json.load(f)


class StartData(BaseModel):
    sector: str


@router.post("/start")
async def start_process(dropdown_choice: StartData, background_tasks: BackgroundTasks):
    tools = [create_node, get_nodes]
    agent = Agent(tools=tools, power=False)
    background_tasks.add_task(agent.create_graph, dropdown_choice.sector)
    return {"status": "success"}


@router.get("/graph")
async def get_graph():
    graph = read_graph()
    return {"node": graph}


@router.get("/demo")
async def demo_nodes():
    second = datetime.now().second
    index = second // 2 + 1

    return {"node": DEMO_DATA[:index]}


@router.post("/converse")
async def chat_about_action(chat_input: ChatInput):
    chatbot = ActionChatbot()
    return chatbot.predict(chat_input)


# @router.post("/items")
# async def create_item(item: Item):
#     print(f"Received item: {item}")
#     return {"Received": item}
