#!/usr/bin/env python3
"""
Test script for the Scrapy-based web scraper.
"""

import asyncio
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from src.tools.web_search_tool import web_search


async def test_web_search():
    """Test the web search function with a simple query."""
    print("Testing web search function...")
    
    # Test query
    query = "Python web scraping tutorial"
    
    try:
        # Use the web search tool
        result = await web_search(query)
        
        print(f"\nQuery: {query}")
        print(f"Found {len(result)} results:")
        
        for url, content in result.items():
            print(f"\nURL: {url}")
            print(f"Content length: {len(content)} characters")
            print(f"Content preview: {content[:200]}...")
            print("-" * 80)
            
    except Exception as e:
        print(f"Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_web_search())