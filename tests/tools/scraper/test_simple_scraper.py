#!/usr/bin/env python3
"""
Test script for the standalone simple web scraper with hardcoded URLs.
"""

import asyncio
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'src'))

from src.tools.scraper.simple_scraper import scrape_urls_async


async def test_simple_scraper():
    """Test the standalone simple web scraper with hardcoded URLs."""
    print("Testing standalone simple web scraper...")
    
    # Test URLs
    test_urls = [
        "https://www.python.org",
        "https://docs.python.org/3/tutorial/",
        "https://scrapy.org/"
    ]
    
    try:
        print(f"Testing with {len(test_urls)} URLs:")
        for url in test_urls:
            print(f"  - {url}")
        
        print(f"\nExtracting content from URLs...")
        
        # Use the simple scraper
        content = await scrape_urls_async(test_urls)
        
        print(f"\nExtracted content from {len(content)} URLs:")
        for url, content_data in content.items():
            print(f"\nURL: {url}")
            if isinstance(content_data, dict):
                title = content_data.get('title', 'No title')
                text_content = content_data.get('content', 'No content')
                status = content_data.get('status', 'Unknown')
                text_length = content_data.get('text_length', 0)
                
                print(f"Status: {status}")
                print(f"Title: {title}")
                print(f"Content length: {text_length} characters")
                print(f"Content preview: {text_content[:200]}...")
            else:
                print(f"Content: {content_data}")
            print("-" * 80)
            
    except Exception as e:
        print(f"Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_simple_scraper()) 