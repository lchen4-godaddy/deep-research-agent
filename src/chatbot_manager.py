import asyncio

from rich.console import Console

from agents import Runner, SQLiteSession

from .agents.chatbot_agent import chatbot_agent

class ChatbotManager:
    # def __init__(self):
        # self.console = Console()
        # self.printer = Printer(self.console)

    async def run(self) -> None:
        session = SQLiteSession("chatbot_session")

        while True:
            try:
                user_input = input("\nYou: ").strip()

                if user_input.lower() in ("exit", "quit", "bye"):
                    print("\nGoodbye!")
                    break
                
                if not user_input:
                    continue
                
                
                chatbot_response = await Runner.run(chatbot_agent, user_input, session=session)
                print(chatbot_response.final_output)

                history = await session.get_items()
                print(history)

                
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                print("Continuing loop...")