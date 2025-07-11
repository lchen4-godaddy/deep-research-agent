import asyncio

from rich.console import Console

from agents import Runner, SQLiteSession

from .agents.chatbot_agent import chatbot_agent

class ChatbotManager:
    # def __init__(self):
        # self.console = Console()
        # self.printer = Printer(self.console)

    async def run(self, query: str) -> None:
        session = SQLiteSession("chatbot_session")

        chatbot_response = await Runner.run(chatbot_agent, query, session=session)
        print(chatbot_response.final_output)

        query = input("-> ")
        chatbot_response = await Runner.run(chatbot_agent, query, session=session)
        print(chatbot_response.final_output)