import asyncio
import json
import signal
import sys
from contextlib import asynccontextmanager

from agents import Runner, SQLiteSession, RunItemStreamEvent

from .custom_session import CustomSession
from .agents.clarification_agent import clarification_agent
from .agents.planner_agent import planner_agent
from .agents.search_plan_agent import search_plan_agent
from .agents.research_agent import research_agent

class TestManager:
    async def run(self) -> None:
        session = CustomSession("test_session")
        
        print("🧪 Test Manager - Individual Agent Testing")
        print("Edit test_manager.py to uncomment the agent you want to test")
        print("Type 'exit' to quit\n")
        
        while True:
            try:
                user_input = input("\n👤 User: ").strip()

                if user_input.lower() in ("exit"):
                    print("\nGoodbye!")
                    sys.exit()
                
                if not user_input:
                    continue
                
                # Uncomment the agent you want to test:
                agent = clarification_agent
                # agent = preplan_agent
                # agent = search_plan_agent
                # agent = research_agent
                
                print(f"\n🔄 Starting {agent.name} agent processing...")
                result = Runner.run_streamed(agent, user_input, session=session)
                current_agent = agent.name
                print(f"🤖 Current Agent: {current_agent}")
                
                # Add timeout to prevent hanging
                try:
                    async with asyncio.timeout(120):  # 2 minute timeout
                        async for event in result.stream_events():
                            # Skip raw response events to reduce console noise
                            if event.type == "raw_response_event":
                                continue
                            
                            # Only show essential events
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
                                print(f"🤖 Final Output: {event.item}")
                except asyncio.TimeoutError:
                    print(f"⏰ Timeout: Agent processing took too long (>2 minutes)")
                    continue
                
                # Debug: Show session memory contents
                print(f"🔍 Session Memory Contents:")
                session_items = await session.get_items()
                for i, item in enumerate(session_items[-3:]):  # Show last 3 items instead of 5
                    print(f"  {i+1}. {type(item).__name__}: {str(item)[:50]}...")
                
                if isinstance(session, CustomSession):
                    # Debug: Show stored tool outputs
                    tool_outputs = await session.get_all_tool_outputs()
                    if tool_outputs:  # Only show if there are tool outputs
                        for tool_name, data in tool_outputs.items():
                            print(f"🔧 Stored: {tool_name} - {str(data)[:50]}...")
                    else:
                        print(f"🔧 No stored tool outputs")
                    
                    # Try to store the tool output manually if we can detect it
                    # Look for tool output events in the stream
                    if hasattr(result, 'new_items'):
                        for item in result.new_items:
                            if hasattr(item, 'type') and item.type == 'tool_call_output_item':
                                if hasattr(item, 'output') and hasattr(item.output, 'idea'):
                                    print(f"🔧 Stored: prewrite_tool - {str(item.output)[:50]}...")
                                    await session.store_tool_output("prewrite_tool", item.output)
                                elif hasattr(item, 'output') and hasattr(item.output, 'searches'):
                                    print(f"🔧 Stored: search_plan_tool - {str(item.output)[:50]}...")
                                    await session.store_tool_output("search_plan_tool", item.output)

                # Print the final result for completeness
                print(f"\n✅ Final Agent Output: {result.final_output}")
                
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                print("Continuing loop...") 