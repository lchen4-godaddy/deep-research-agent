#!/usr/bin/env python3
"""
Test script for the plan_writer_tool with LLM call for human validation.
"""

import asyncio
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from src.agent_memory import AGENT_MEMORY
from src.tool_agents.planner.plan_writer_tool import plan_writer_tool

async def test_plan_writer_tool():
    """Test the plan_writer_tool with LLM call for human validation."""
    
    # Clear any existing data
    await AGENT_MEMORY.clear_research_plan()
    await AGENT_MEMORY.clear_items()
    
    # Create test conversation context
    test_context = """
    User: I want to start a business selling organic coffee beans online.
    I'm thinking of targeting health-conscious consumers who prefer organic products.
    I need to understand the market, competition, and pricing strategies.
    I also want to know about the legal requirements for selling food products online.
    """
    
    # Store the conversation context in agent memory
    await AGENT_MEMORY.store_item("conversation", test_context)
    
    print("Starting plan_writer_tool test...")
    print(f"Test context: {test_context}")
    print("-" * 50)
    
    try:
        # Test the plan_writer_tool
        result = await plan_writer_tool()
        
        print("Plan writer tool completed!")
        print(f"Result: {result}")
        print("-" * 50)
        
        # Get the generated research plan
        research_plan = await AGENT_MEMORY.get_research_plan()
        
        print("Generated Research Plan:")
        print("=" * 50)
        print(research_plan)
        print("=" * 50)
        
        print("\nLLM Output for Human Validation:")
        print("The plan_writer_tool has generated a research plan based on the provided context.")
        print("Please review the output above to validate the quality and completeness of the plan.")
        
    except Exception as e:
        print(f"Error during plan writing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_plan_writer_tool()) 