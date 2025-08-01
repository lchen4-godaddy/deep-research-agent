#!/usr/bin/env python3
"""
Test script for the research tool with a single research question.
"""

import asyncio
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from src.agent_memory import AGENT_MEMORY
from src.tools.researcher_tool import researcher

async def test_researcher():
    """Test the research tool with a single research question."""
    
    # Clear any existing data
    await AGENT_MEMORY.clear_research_dump()
    await AGENT_MEMORY.clear_research_plan()
    
    # Create a simple research plan with one question
    test_plan = """
    Research Plan:
    
    1. What are the latest developments in artificial intelligence in 2024?
    
    Please research this question thoroughly and provide comprehensive findings.
    """
    
    # Store the plan in agent memory
    await AGENT_MEMORY.store_research_plan(test_plan)
    
    print("Starting research tool test...")
    print(f"Research plan: {test_plan}")
    print("-" * 50)
    
    try:
        # Test the researcher tool with a single research question
        test_question = "What are the latest developments in artificial intelligence in 2024?"
        result = await researcher(test_question)
        
        print("Research tool completed!")
        print(f"Result: {result}")
        print("-" * 50)
        
        # Check what was stored in research dump
        research_dump = await AGENT_MEMORY.get_from_research_dump_by_question(test_question)
        
        print(f"Research dump entries: {len(research_dump)}")
        for i, ((title, url), summary) in enumerate(research_dump[:3]):  # Show first 3 entries
            print(f"Entry {i+1}:")
            print(f"  Title: {title}")
            print(f"  URL: {url}")
            print(f"  Summary: {summary[:200]}...")  # Truncate long summaries
            print()
            
    except Exception as e:
        print(f"Error during research: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_researcher()) 