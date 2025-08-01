#!/usr/bin/env python3
"""
Test script for the research_tool with LLM call for human validation.
"""

import asyncio
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from src.agent_memory import AGENT_MEMORY
from src.tool_agents.research.research_tool import research_tool

async def test_research_tool():
    """Test the research_tool with LLM call for human validation."""
    
    # Clear any existing data
    await AGENT_MEMORY.clear_research_plan()
    await AGENT_MEMORY.clear_research_dump()
    
    # Create a test research plan with simple questions
    test_plan = """
    # Research Plan for AI Technology
    
    ## Information
    - Product Name: AI-Powered Research Assistant
    - Description: An AI tool that helps researchers and students conduct comprehensive research
    - Features & Scope: Web search, summarization, citation management
    
    ## Research Areas
    
    ### Market Analysis
    - Sub-topics: Industry Trends, Target Audience, Competitors
    - Summary: Explore the AI research tools market and identify opportunities
    - Research Question: What are the latest developments in AI research tools in 2024?
    
    ### Business Model & Financial Research
    - Sub-topics: Pricing, Revenue Streams, Market Size
    - Summary: Analyze the business potential of AI research tools
    - Research Question: What is the market size for AI-powered research tools?
    """
    
    # Store the research plan in agent memory
    await AGENT_MEMORY.store_research_plan(test_plan)
    
    print("Starting research_tool test...")
    print(f"Test research plan: {test_plan}")
    print("-" * 50)
    
    try:
        # Test the research_tool
        result = await research_tool()
        
        print("Research tool completed!")
        print(f"Result: {result}")
        print("-" * 50)
        
        # Check what was stored in research dump
        all_research_dump = await AGENT_MEMORY.get_research_dump()
        
        print(f"Research dump entries: {len(all_research_dump)}")
        for question, entries in all_research_dump.items():
            print(f"\nResearch Question: {question}")
            print(f"Number of sources: {len(entries)}")
            for i, ((title, url), summary) in enumerate(entries[:2]):  # Show first 2 entries
                print(f"  Source {i+1}:")
                print(f"    Title: {title}")
                print(f"    URL: {url}")
                print(f"    Summary: {summary[:200]}...")  # Truncate long summaries
                print()
        
        print("LLM Output for Human Validation:")
        print("The research_tool has conducted research on the provided questions.")
        print("Please review the output above to validate the quality and relevance of the research results.")
        
    except Exception as e:
        print(f"Error during research: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_research_tool()) 