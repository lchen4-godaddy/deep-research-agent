#!/usr/bin/env python3
"""
Test script for the query_writer_tool with LLM call for human validation.
"""

import asyncio
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from src.tool_agents.research.query_writer_tool import query_writer_tool

async def test_query_writer_tool():
    """Test the query_writer_tool with LLM call for human validation."""
    
    # Test research questions
    test_questions = [
        "What are the latest developments in artificial intelligence in 2024?",
        "What is the market size for electric vehicles in the United States?",
        "What are the best practices for remote work productivity?",
        "What are the environmental impacts of renewable energy technologies?"
    ]
    
    print("Starting query_writer_tool test...")
    print("-" * 50)
    
    try:
        for i, question in enumerate(test_questions, 1):
            print(f"\nTest {i}: {question}")
            print("-" * 30)
            
            # Test the query_writer_tool
            result = await query_writer_tool(question)
            
            print(f"Generated search queries:")
            for j, query in enumerate(result, 1):
                print(f"  {j}. {query}")
            
            print(f"Total queries generated: {len(result)}")
            print()
        
        print("LLM Output for Human Validation:")
        print("The query_writer_tool has generated search queries for each research question.")
        print("Please review the output above to validate the quality and relevance of the generated queries.")
        
    except Exception as e:
        print(f"Error during query writing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_query_writer_tool()) 