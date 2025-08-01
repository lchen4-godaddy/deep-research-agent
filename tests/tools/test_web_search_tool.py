#!/usr/bin/env python3
"""
Test script for the web_search_tool with LLM call for human validation.
"""

import asyncio
from dotenv import load_dotenv
from unittest.mock import patch, MagicMock

# Load environment variables from .env file
load_dotenv()

from src.tools.web_search_tool import web_search_tool, web_search, source_finder

async def test_web_search_tool():
    """Test the web_search_tool with LLM call for human validation."""
    
    # Test search queries
    test_queries = [
        "latest developments in artificial intelligence 2024",
        "electric vehicle market trends United States",
        "remote work productivity best practices"
    ]
    
    print("Starting web_search_tool test...")
    print("-" * 50)
    
    try:
        for i, query in enumerate(test_queries, 1):
            print(f"\nTest {i}: {query}")
            print("-" * 30)
            
            # Test the web_search_tool
            result = await web_search_tool(query)
            
            print(f"Search results for '{query}':")
            print(f"Number of sources found: {len(result)}")
            
            for j, ((title, url), summary) in enumerate(result[:2], 1):  # Show first 2 results
                print(f"\n  Source {j}:")
                print(f"    Title: {title}")
                print(f"    URL: {url}")
                print(f"    Summary: {summary[:200]}...")  # Truncate long summaries
                print()
        
        print("LLM Output for Human Validation:")
        print("The web_search_tool has conducted web searches and generated summaries for each query.")
        print("Please review the output above to validate the quality and relevance of the search results and summaries.")
        
    except Exception as e:
        print(f"Error during web search: {e}")
        import traceback
        traceback.print_exc()

def test_source_finder():
    """Test the source_finder function with mock data."""
    
    print("Testing source_finder function...")
    
    # Test with mock DDGS results
    mock_results = [
        {'href': 'https://example1.com', 'title': 'Example 1'},
        {'href': 'https://example2.com', 'title': 'Example 2'},
        {'href': 'https://example3.com', 'title': 'Example 3'}
    ]
    
    with patch('src.tools.web_search_tool.DDGS') as mock_ddgs:
        mock_ddgs_instance = MagicMock()
        mock_ddgs_instance.text.return_value = mock_results
        mock_ddgs.return_value = mock_ddgs_instance
        
        result = source_finder("test query")
        
        print(f"Source finder result: {result}")
        assert len(result) == 3
        assert all(url.startswith('https://') for url in result)
        print("Source finder test passed!")

async def test_web_search_integration():
    """Test the web_search function with mock scraping."""
    
    print("\nTesting web_search function with mock data...")
    
    # Mock data for testing
    mock_urls = [
        "https://example1.com",
        "https://example2.com"
    ]
    
    mock_scraped_data = [
        ("Example Page 1", "This is the content of example page 1 with some information about AI."),
        ("Example Page 2", "This is the content of example page 2 with information about technology trends.")
    ]
    
    with patch('src.tools.web_search_tool.source_finder') as mock_source_finder, \
         patch('src.tools.web_search_tool.scrape_url') as mock_scrape_url, \
         patch('src.tools.web_search_tool.contextual_summary_tool') as mock_summary:
        
        mock_source_finder.return_value = mock_urls
        mock_scrape_url.side_effect = mock_scraped_data
        mock_summary.side_effect = lambda query, content: f"Summary of: {content[:50]}..."
        
        result = await web_search("test query")
        
        print(f"Web search result: {len(result)} sources")
        for (title, url), summary in result:
            print(f"  Title: {title}")
            print(f"  URL: {url}")
            print(f"  Summary: {summary}")
            print()
        
        print("Web search integration test passed!")

if __name__ == "__main__":
    # Run unit tests first
    test_source_finder()
    
    # Run integration test
    asyncio.run(test_web_search_integration())
    
    # Run main test with real LLM calls
    asyncio.run(test_web_search_tool()) 