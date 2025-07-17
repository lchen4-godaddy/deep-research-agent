import asyncio
import sys
from contextlib import asynccontextmanager

from agents import Runner, SQLiteSession, RunItemStreamEvent

from .custom_session import CustomSession
from .agents.triage_agent import triage_agent
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

                if user_input.lower() in ("exit"):
                    print("\nGoodbye!")
                    sys.exit()
                
                if not user_input:
                    continue

                # Use streaming to capture tool outputs and agent responses with timeout
                print(f"\n🔄 Starting agent processing...")
                result = Runner.run_streamed(triage_agent, user_input, session=session)
                current_agent = "TriageAgent"
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
                                elif event.name == "message_output_created":
                                    print(f"💬 Message Output Event Detected!")
                                elif event.name == "handoff_occured":
                                    # Track agent handoffs
                                    if hasattr(event.item, 'target_agent') and hasattr(event.item, 'source_agent'):
                                        source_agent = event.item.source_agent.name
                                        target_agent = event.item.target_agent.name
                                        print(f"🤝 Agent Handoff: {source_agent} → {target_agent}")
                                        current_agent = target_agent
                                        print(f"🤖 Current Agent: {current_agent}")
                                    else:
                                        print(f"❌ No target_agent or source_agent attribute found in handoff event")
                                elif event.name == "handoff_requested":
                                    # Show when handoff is requested
                                    print(f"❓ Handoff Requested: {current_agent}")
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
                            print(f"🔧 Stored: {tool_name} - {str(data)}")
                    else:
                        print(f"🔧 No stored tool outputs")
                    
                    # Try to store the tool output manually if we can detect it
                    # Look for tool output events in the stream
                    if hasattr(result, 'new_items'):
                        for item in result.new_items:
                            if hasattr(item, 'type') and item.type == 'tool_call_output_item':
                                if hasattr(item, 'output') and hasattr(item.output, 'idea'):
                                    print(f"🔧 Stored: prewrite_tool")
                                    print(f"   Content: {item.output}")
                                    await session.store_tool_output("prewrite_tool", item.output)
                                elif hasattr(item, 'output') and hasattr(item.output, 'searches'):
                                    print(f"🔧 Stored: search_plan_tool")
                                    print(f"   Content: {item.output}")
                                    await session.store_tool_output("search_plan_tool", item.output)
                                elif hasattr(item, 'output') and hasattr(item.output, 'executive_summary') and hasattr(item.output, 'key_findings'):
                                    print(f"🔧 Stored: simple_report_tool")
                                    print(f"   Executive Summary: {item.output.executive_summary[:100]}...")
                                    await session.store_tool_output("simple_report_tool", item.output)
                                elif hasattr(item, 'output') and hasattr(item.output, 'executive_summary') and hasattr(item.output, 'key_insights'):
                                    print(f"🔧 Stored: research_report_tool")
                                    print(f"   Executive Summary: {item.output.executive_summary[:100]}...")
                                    await session.store_tool_output("research_report_tool", item.output)
                                elif hasattr(item, 'output') and isinstance(item.output, str) and len(item.output) > 50:
                                    # Likely research_tool output (string research summary)
                                    print(f"🔧 Stored: research_tool")
                                    print(f"   Research Summary: {item.output[:100]}...")
                                    await session.store_tool_output("research_tool", item.output)
                                else:
                                    # Generic fallback for any other tool output
                                    print(f"🔧 Stored: unknown_tool")
                                    print(f"   Content: {str(item.output)[:100]}...")
                                    await session.store_tool_output("unknown_tool", item.output)

                # Print the final result for completeness
                print(f"\n✅ Final Agent Output: {result.final_output}")
                
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                print("Continuing loop...")