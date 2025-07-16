import asyncio
import json

from agents import Runner, SQLiteSession, RunItemStreamEvent

from .custom_session import CustomSession
from .agents.preplan_agent import preplan_agent

class Manager:
    # def __init__(self):
        # self.console = Console()
        # self.printer = Printer(self.console)

    async def run(self) -> None:
        session = CustomSession("deep_research_session")
        
        while True:
            try:
                user_input = input("\n👤 User: ").strip()

                if user_input.lower() in ("exit", "quit", "bye"):
                    print("\nGoodbye!")
                    break
                
                if not user_input:
                    continue
                
                # chatbot_response = await Runner.run(preplan_agent, user_input, session=session)
                # print(chatbot_response.final_output)

                # history = await session.get_items()
                # print(history)

                # Use streaming to capture tool outputs and agent responses
                result = Runner.run_streamed(preplan_agent, user_input, session=session)
                async for event in result.stream_events():
                    # Skip raw response events to reduce console noise
                    if event.type == "raw_response_event":
                        continue
                    
                    # Debug: Print all events to see what's happening
                    print(f"\n🔍 Event: {event.type} - {getattr(event, 'name', 'N/A')}")
                    
                    if event.type == "run_item_stream_event":
                        if event.name == "tool_called":
                            print(f"🔧 Tool Called Event Detected!")
                        elif event.name == "tool_output":
                            print(f"📤 Tool Output Event Detected!")
                            # Print the actual tool output data
                            print(f"🔍 Tool Output Item: {event.item}")
                        elif event.name == "message_output_created":
                            print(f"💬 Message Output Event Detected!")
                    elif event.type == "final_output":
                        print(f"\n🤖 Final Output: {event.item}")
                
                # Also print the final result for completeness
                print(f"\n📋 Final Agent Output: {result.final_output}")
                
                # Debug: Show session memory contents
                print(f"\n🔍 Session Memory Contents:")
                session_items = await session.get_items()
                for i, item in enumerate(session_items[-5:]):  # Show last 5 items
                    print(f"  {i+1}. {type(item).__name__}: {str(item)[:100]}...")
                
                if isinstance(session, CustomSession):
                    # Debug: Show stored tool outputs
                    print(f"\n🔧 Stored Tool Outputs:")
                    tool_outputs = await session.get_all_tool_outputs()
                    for tool_name, data in tool_outputs.items():
                        print(f"  {tool_name}: {data}")
                    
                    # Try to store the tool output manually if we can detect it
                    # Look for tool output events in the stream
                    if hasattr(result, 'new_items'):
                        for item in result.new_items:
                            if hasattr(item, 'type') and item.type == 'tool_call_output_item':
                                if hasattr(item, 'output') and hasattr(item.output, 'idea'):
                                    print(f"🔧 Detected prewrite tool output, storing...")
                                    await session.store_tool_output("prewrite_tool", item.output)
                                    print(f"✅ Stored prewrite tool output")

                
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                print("Continuing loop...")