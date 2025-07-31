#!/usr/bin/env python3
"""
Simple test script for the research tool components.
"""

import asyncio
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.agent_memory import AGENT_MEMORY
from src.tool_agents.research.query_writer_tool import query_writer_tool
from src.tools.web_search_tool import web_search_tool

async def test_research_components():
    """Test the individual components of the research tool."""
    
    # Clear any existing data
    await AGENT_MEMORY.clear_tool_outputs()
    await AGENT_MEMORY.clear_research_dump()
    
    test_question = "What are the latest developments in artificial intelligence in 2024?"
    
    print("Testing research tool components...")
    print(f"Research question: {test_question}")
    print("-" * 50)
    
    try:
        # Test 1: Query writer tool
        print("1. Testing query writer tool...")
        queries = await query_writer_tool(test_question)
        print(f"Generated queries: {queries}")
        print()
        
        # Test 2: Web search tool (with first query)
        if queries:
            print("2. Testing web search tool...")
            first_query = queries[0]
            print(f"Using query: {first_query}")
            results = await web_search_tool(first_query)
            print(f"Found {len(results)} results")
            
            # Show first result
            if results:
                url, summary = results[0]
                print(f"First result URL: {url}")
                print(f"First result summary: {summary[:200]}...")
                print()
                
                # Test 3: Store in research dump
                print("3. Testing research dump storage...")
                await AGENT_MEMORY.add_to_research_dump(test_question, results)
                
                # Test 4: Retrieve from research dump
                print("4. Testing research dump retrieval...")
                stored_results = await AGENT_MEMORY.get_from_research_dump_by_question(test_question)
                print(f"Retrieved {len(stored_results)} results from research dump")
                
                print("\n✅ All components working!")
                
            else:
                print("❌ No results found from web search")
        else:
            print("❌ No queries generated")
            
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_research_components()) 