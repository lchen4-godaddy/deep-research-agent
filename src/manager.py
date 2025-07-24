import asyncio
import sys
from typing import Any

from agents import Runner

from .main_agents.triage_agent import triage_agent
from .globals import CURRENT_SESSION as session

class Manager:
    def _get_tool_name(self, event_item: Any) -> str:
        """Extract tool name from event item using concrete type checks."""
        # Check if it's a dictionary with 'name' key
        if isinstance(event_item, dict):
            if 'name' in event_item:
                return str(event_item['name'])
            if 'tool_name' in event_item:
                return str(event_item['tool_name'])
            # Check for nested tool structure
            for key in ['tool', 'function', 'call']:
                if key in event_item:
                    tool_obj = event_item[key]
                    if isinstance(tool_obj, dict) and 'name' in tool_obj:
                        return str(tool_obj['name'])
            raise ValueError(f"Tool name not found in dictionary: {event_item}")
        
        # Check if it has a raw_item attribute that's a dictionary
        if hasattr(event_item, 'raw_item'):
            raw_item = event_item.raw_item
            if isinstance(raw_item, dict):
                if 'name' in raw_item:
                    return str(raw_item['name'])
                if 'tool_name' in raw_item:
                    return str(raw_item['tool_name'])
            # If raw_item is an object with name attribute
            elif not isinstance(raw_item, dict) and hasattr(raw_item, 'name'):
                return str(raw_item.name)
            raise ValueError(f"Tool name not found in raw_item: {raw_item}")
        
        # Check if the item itself has a name attribute
        if not isinstance(event_item, dict) and hasattr(event_item, 'name'):
            return str(event_item.name)
        
        # Check if it has a tool_name attribute
        if not isinstance(event_item, dict) and hasattr(event_item, 'tool_name'):
            return str(event_item.tool_name)
        
        # Check for nested object structure
        for attr_name in ['tool', 'function', 'call']:
            if not isinstance(event_item, dict) and hasattr(event_item, attr_name):
                tool_obj = getattr(event_item, attr_name)
                if isinstance(tool_obj, dict) and 'name' in tool_obj:
                    return str(tool_obj['name'])
                elif not isinstance(tool_obj, dict) and hasattr(tool_obj, 'name'):
                    return str(tool_obj.name)
        
        raise ValueError(f"Tool name not found in event item: {type(event_item)} - {event_item}")

    def _get_agent_names(self, event_item: Any) -> tuple[str, str]:
        """Extract source and target agent names from handoff event using concrete type checks."""
        source_agent = None
        target_agent = None
        
        # Check if it's a dictionary
        if isinstance(event_item, dict):
            if 'source_agent' in event_item:
                source_obj = event_item['source_agent']
                if isinstance(source_obj, dict) and 'name' in source_obj:
                    source_agent = str(source_obj['name'])
                elif not isinstance(source_obj, dict) and hasattr(source_obj, 'name'):
                    source_agent = str(source_obj.name)
                else:
                    raise ValueError(f"Source agent name not found in: {source_obj}")
            
            if 'target_agent' in event_item:
                target_obj = event_item['target_agent']
                if isinstance(target_obj, dict) and 'name' in target_obj:
                    target_agent = str(target_obj['name'])
                elif not isinstance(target_obj, dict) and hasattr(target_obj, 'name'):
                    target_agent = str(target_obj.name)
                else:
                    raise ValueError(f"Target agent name not found in: {target_obj}")
        
        # Check if it has source_agent and target_agent attributes
        else:
            if hasattr(event_item, 'source_agent'):
                source_obj = event_item.source_agent
                if isinstance(source_obj, dict) and 'name' in source_obj:
                    source_agent = str(source_obj['name'])
                elif not isinstance(source_obj, dict) and hasattr(source_obj, 'name'):
                    source_agent = str(source_obj.name)
                else:
                    raise ValueError(f"Source agent name not found in: {source_obj}")
            
            if hasattr(event_item, 'target_agent'):
                target_obj = event_item.target_agent
                if isinstance(target_obj, dict) and 'name' in target_obj:
                    target_agent = str(target_obj['name'])
                elif not isinstance(target_obj, dict) and hasattr(target_obj, 'name'):
                    target_agent = str(target_obj.name)
                else:
                    raise ValueError(f"Target agent name not found in: {target_obj}")
        
        if source_agent is None or target_agent is None:
            raise ValueError(f"Could not extract agent names from: {event_item}")
        
        return source_agent, target_agent

    async def run(self) -> None:
        """Main agent loop."""

        print("Welcome to the Deep Research Assistant for business development. What business or product idea do you have in mind?")

        # Add initial message to the session
        await session.add_items([{"role": "system", "content": "Welcome to the Deep Research Assistant for business development. What business or product idea do you have in mind?"}])

        # Add initial message to the session
        await session.add_items([{"role": "system", "content": "Welcome to the Deep Research Assistant for business development. What business or product idea do you have in mind?"}])
        
        # User-agent loop
        while True:
            try:
                user_input = input("\n👤 User: ").strip()

                if user_input.lower() in ("exit"):
                    print("\nGoodbye!")
                    sys.exit()
                
                if not user_input:
                    continue

                # Use streaming to capture tool outputs and agent responses with timeout
                # print(f"\n🔄 Starting agent processing...")
                # result = Runner.run_streamed(triage_agent, user_input, session=session)
                # current_agent = "TriageAgent"
                # print(f"🤖 Current Agent: {current_agent}")
                
                result = Runner.run_streamed(triage_agent, user_input, session=session)
                current_agent = "TriageAgent"

                # Add timeout to prevent hanging
                try:
                    tool_call_map = {}  # Map call_id to tool_name
                    
                    async with asyncio.timeout(120):  # 2 minute timeout
                        async for event in result.stream_events():
                            # Skip raw response events to reduce console noise
                            if event.type == "raw_response_event":
                                continue
                            
                            # Debug: Log all events to understand the structure (verbose)
                            # print(f"🔍 DEBUG: Event type='{event.type}', name='{getattr(event, 'name', 'N/A')}', item_type='{type(getattr(event, 'item', None)).__name__}'")
                            
                            # Only show essential events
                            if event.type == "run_item_stream_event":
                                if event.name == "tool_called":

                                    # Debug: Show the full event item content (verbose)
                                    # print(f"🔍 DEBUG: tool_called event item: {getattr(event, 'item', 'NO_ITEM')}")
                                    
                                    # Extract tool name using concrete type checking
                                    try:
                                        tool_name = self._get_tool_name(event.item)
                                        print(f"🔧 Tool Called: {tool_name}")
                                        
                                        # Extract call_id to map with output
                                        tool_item = getattr(event, 'item', None)
                                        if tool_item and hasattr(tool_item, 'raw_item'):
                                            raw_item = tool_item.raw_item
                                            if hasattr(raw_item, 'call_id'):
                                                call_id = raw_item.call_id
                                                tool_call_map[call_id] = tool_name
                                                print(f"🔗 Mapped call_id {call_id} to tool {tool_name}")
                                    except ValueError as e:
                                        print(f"❌ Error extracting tool name: {e}")
                                elif event.name == "tool_output":
                                    # Tool output events contain the output data, not the tool name
                                    # We can extract the call_id to match with the tool call
                                    output_item = getattr(event, 'item', None)
                                    if output_item and hasattr(output_item, 'raw_item'):
                                        raw_item = output_item.raw_item
                                        if isinstance(raw_item, dict) and 'call_id' in raw_item:
                                            call_id = raw_item['call_id']
                                            tool_name = tool_call_map.get(call_id, "unknown_tool")
                                            print(f"📤 Tool Output for {tool_name} (call_id: {call_id})")
                                        else:
                                            print(f"📤 Tool Output received (no call_id found)")
                                    else:
                                        print(f"📤 Tool Output received")
                                elif event.name == "message_output_created":
                                    print(f"💬 Message Output Event Detected!")
                                elif event.name == "handoff_occured":
                                    # Track agent handoffs using concrete type checking
                                    try:
                                        source_agent, target_agent = self._get_agent_names(event.item)
                                        print(f"🤝 Agent Handoff: {source_agent} → {target_agent}")
                                        current_agent = target_agent
                                        print(f"🤖 Current Agent: {current_agent}")
                                    except ValueError as e:
                                        print(f"❌ Error extracting agent names: {e}")
                                elif event.name == "handoff_requested":
                                    # Show when handoff is requested
                                    print(f"❓ Handoff Requested: {current_agent}")
                except asyncio.TimeoutError:
                    print(f"⏰ Timeout: Agent processing took too long (>2 minutes)")
                    continue
                
                # Debug: Show session memory contents
                print(f"🔍 Session Conversation History:")
                session_items = await session.get_items()
                for i, item in enumerate(session_items[-5:]):  # Show last 5 items
                    print(f"  {i+1}. {type(item).__name__}: {str(item)[:150]}...")
                
                # Debug: Show stored tool outputs
                print(f"🔍 Session Stored Tool Outputs:")
                tool_outputs = await session.get_all_tool_outputs()
                if tool_outputs:  # Only show if there are tool outputs
                    for tool_name, data in tool_outputs.items():
                        print(f"🔧 {tool_name} - {str(data)}...")
                else:
                    print(f"🗋 No stored tool outputs")
                
                # Print the final result for completeness
                print(f"\n✅ Final Agent Output: {result.final_output}")
                
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                print("Continuing loop...")