#!/usr/bin/env python3
"""
Test script for the web search tool components (source_finder and web_content_extractor).
"""

import asyncio
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from src.tools.web_search_tool import source_finder, web_content_extractor


async def test_web_search_components():
    """Test the web search tool components with a simple query."""
    print("Testing web search tool components...")
    
    # Test query
    query = "Python web scraping tutorial"
    
    try:
        # Find URLs
        urls = source_finder(query)
        
        if urls is None:
            print("source_finder returned None")
            return
            
        print(f"Found {len(urls)} URLs:")
        for url in urls:
            print(f"  - {url}")
        
        if urls:
            # Extract content from the first few URLs
            test_urls = urls[:3]  # Test with first 3 URLs
            print(f"\nExtracting content from {len(test_urls)} URLs...")
            
            content = await web_content_extractor(test_urls)
            
            print(f"\nExtracted content from {len(content)} URLs:")
            for url, content_text in content.items():
                print(f"\nURL: {url}")
                print(f"Content length: {len(content_text)} characters")
                print(f"Content preview: {content_text[:200]}...")
                print("-" * 80)
        else:
            print("No URLs found for the query")
            
    except Exception as e:
        print(f"Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_web_search_components()) 