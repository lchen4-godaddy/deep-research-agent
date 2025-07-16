import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from .research_manager import ResearchManager
from .chatbot_manager import ChatbotManager
from .manager import Manager
from .test_manager import TestManager


async def main() -> None:
    # await ResearchManager().run(query)
    # await ChatbotManager().run()
    print("Welcome to the Deep Research Assistant for business development. What business or product idea do you have in mind?")
    await Manager().run()
    # await TestManager().run()


if __name__ == "__main__":
    asyncio.run(main())
