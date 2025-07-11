import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from .manager import ResearchManager
from .chatbot_manager import ChatbotManager


async def main() -> None:
    print("Welcome to my test chatbot. What would you like to talk about?")
    #query = input("-> ")
    # await ResearchManager().run(query)
    await ChatbotManager().run()


if __name__ == "__main__":
    asyncio.run(main())
