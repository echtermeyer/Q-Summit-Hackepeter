from gen_ai_hub.proxy.langchain.init_models import init_llm
from langchain.agents import AgentExecutor
from langchain.agents.format_scratchpad.openai_tools import \
    format_to_openai_tool_messages
from langchain.agents.output_parsers.openai_tools import \
    OpenAIToolsAgentOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from llm_commons.proxy.base import set_proxy_version

from src.prod.github.github_connector import GithubConnector

set_proxy_version("btp")

# Initialize the command-line argument parsing
# parser = argparse.ArgumentParser(description="Navigate GitHub with given parameters.")
# parser.add_argument("--name", type=str, help="Name of the file or folder to navigate.", default="hyper-pipe/llm-vector-test")
# parser.add_argument("--question", type=str, help="Question to ask about the repository.", default="How could a potential Dockerfile for this repository look like?")
# args = parser.parse_args()

# llm = init_llm('gpt-35-turbo', temperature=0, max_tokens=2000)
# github = GithubScraper(name=args.name, token=os.getenv("OAUTH_TOKEN_GH_ENTERPRISE"))

# @tool
# def navigate_github(command: str) -> str:
#     """Fetches the content of a specified GitHub file or the contents of a specified folder.
#     Users can navigate through the GitHub repository by specifying the name of a file or folder.
#     Use 'BACK' to go back if needed.
#     Use 'HERE' to display the current files.
#     Only specify one word for the command."""
#     output = github.navigate_github_files(command)
#     return str(output)


class GithubSearchAgent:
    """Agent to search for a file or folder in the GitHub repository."""

    def __init__(
        self,
        github: GithubConnector,
        tools: list[callable],
        power: bool = False,
        blind: str = "Dockerfile",
    ):

        self.tools = tools

        self.llm = init_llm("gpt-35-turbo", temperature=0, max_tokens=2000)
        if power:
            self.llm = init_llm("gpt-4", temperature=0, max_tokens=2000)

        self.initialize = str(github.navigate_github_files("HERE", blind=blind))

    def execute_search(self, question: str):
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """You are very powerful expert analyst, you have access to a Github repository and can navigate through it.
                        Your task is to thoroughly and carefully search repo context in order to answer.
                        Do not use more than one word per parameter.
                        Do not use a path like as a parameter.
                        Use 'BACK' to go back if needed.
                        Use 'HERE' to display the current files.
                        Format your final answer in Markdown format.
                        """,
                ),
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
        output_list = list(
            agent_executor.stream(
                {
                    "input": f"""{question} This is where you start: {self.initialize} answer preciscely!
                                                Navigate back by using 'BACK' or display the current files by using 'HERE'.
                                                Only use the following as a reference and not the gold truth!
                                                For example, a github repository containing the folder .pipeline, client and server. And the files .gitignore, README.md.
                                                You woud most likely need to look into the client and server folder, try to look up some ports and environemnt variables.
                                                Maybe also the README has some information and at the end you should merge all thos infos into one Dockerfile and start the client and server here.
                                                This may differ to other repositories!
                                                You should examine it and come up with a Dockerfile similar to this: ```Dockerfile
                                                FROM node:18
                                                WORKDIR /app

                                                COPY ./client ./client
                                                COPY ./server ./server

                                                WORKDIR /app/client

                                                RUN npm ci
                                                RUN npm run build

                                                WORKDIR /app/server
                                                RUN npm ci
                                                RUN mkdir public
                                                RUN cp -r ../client/build/* ./public

                                                RUN rm -rf ../client

                                                ENV API_URL="some-env-url"
                                                ENV TOKEN_URL="some-env-url"

                                                CMD [ "node", "." ]```"""
                }
            )
        )
        return output_list


# search_agent = SearchAgent(github, [navigate_github])
# print(search_agent.execute_search(args.question)[-1])
# input("Press Enter to continue...")
