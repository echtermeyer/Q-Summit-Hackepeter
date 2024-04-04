from typing import List

from dotenv import load_dotenv
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.memory import ChatMessageHistory
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

load_dotenv()


class ChatInput(BaseModel):
    science: str
    sources: List[str]
    history: List[dict]


class ActionChatbot:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.5)

    def predict(self, chat_input: ChatInput):
        history = ChatMessageHistory()

        initial_message = f"""
        You are an expert AI model capable of answering questions about evidence-based questions.

        You have been given the following information: {chat_input.science}.
        This information is from the following sources: {chat_input.sources}.

        When answering a questions, answer based on the provided information.
        Come up with digits that sound plausible, but do not worry about being exact.
        Always provide a source for your answer, doesnt matter if it is a real source or not. Try to use every source once.
        """

        history.add_user_message(initial_message)

        for entity in chat_input.history:
            if "user" in entity.keys():
                history.add_user_message(entity["user"])
            elif "model" in entity.keys():
                history.add_ai_message(entity["model"])
            else:
                raise ValueError("FUCK YOU")

        conversation = ConversationChain(
            llm=self.llm, memory=ConversationBufferMemory(chat_memory=history)
        )

        response = conversation(chat_input.history[-1]["user"])
        return response["response"]
