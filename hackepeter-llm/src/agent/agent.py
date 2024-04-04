from langchain.agents import AgentExecutor
from langchain.agents.format_scratchpad.openai_tools import \
    format_to_openai_tool_messages
from langchain.agents.output_parsers.openai_tools import \
    OpenAIToolsAgentOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

from src.agent.prompts import system_prompt, user_prompt


class Agent:
    def __init__(self, tools: list[callable], power: bool = False):
        self.tools = tools
        self.system_prompt = system_prompt
        self.user_prompt = user_prompt

        model = "gpt-4-turbo-preview" if power else "gpt-3.5-turbo"
        self.llm = ChatOpenAI(model_name=model, temperature=0)

    def create_graph(self, dropdown_choice: str):
        system_prompt = self.system_prompt.format(dropdown_choice=dropdown_choice)
        user_prompt = self.user_prompt.format()

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("user", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )

        llm_with_tools = self.llm.bind_tools(self.tools)

        agent = (
            {
                "input": lambda x: x["input"],
                "agent_scratchpad": lambda x: format_to_openai_tool_messages(
                    x["intermediate_steps"]
                ),
            }
            | prompt
            | llm_with_tools
            | OpenAIToolsAgentOutputParser()
        )

        agent_executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=True,
            early_stopping_method="generate",
        )

        # Execute and print the last output
        output_list = list(agent_executor.stream({"input": user_prompt}))
