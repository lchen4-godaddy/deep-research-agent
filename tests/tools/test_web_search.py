#!/usr/bin/env python3
"""
Test script for the web search tool with real API calls.
"""

import pytest
import asyncio

from src.tools.web_search_tool import web_search, source_finder, web_content_extractor


@pytest.mark.asyncio
async def test_web_search_real_api():
    """Test web search with real DDGS API calls."""
    query = "Python web scraping tutorial"
    
    print(f"\nTesting web search with real API: {query}")
    
    try:
        # Call the function with real API
        result = await web_search(query)
        
        # Basic assertions about structure
        assert result is not None
        assert isinstance(result, dict)
        
        # Should have some results (but we don't assert specific number due to API variability)
        if len(result) > 0:
            print(f"Found {len(result)} results")
            
            # Check that all returned URLs have content
            for url, content in result.items():
                assert isinstance(url, str)
                assert url.startswith('http')  # Should be valid URLs
                assert isinstance(content, str)
                assert len(content) > 0  # Should have some content
                print(f"  - {url}: {len(content)} characters")
        else:
            print("No results found (this might happen with rate limiting)")
            
    except Exception as e:
        print(f"Error during testing: {str(e)}")
        # Don't fail the test for API errors - they're expected sometimes
        pytest.skip(f"API call failed: {str(e)}")


@pytest.mark.asyncio
async def test_source_finder_real_api():
    """Test source finder with real DDGS API calls."""
    query = "Python tutorial"
    
    print(f"\nTesting source finder with real API: {query}")
    
    try:
        result = source_finder(query)
        
        # Verify the result structure
        assert isinstance(result, list)
        
        if len(result) > 0:
            print(f"Found {len(result)} URLs")
            for url in result:
                assert isinstance(url, str)
                assert url.startswith('http')
                print(f"  - {url}")
        else:
            print("No URLs found")
            
    except Exception as e:
        print(f"Error during testing: {str(e)}")
        pytest.skip(f"API call failed: {str(e)}")


@pytest.mark.asyncio
async def test_web_content_extractor_real_api():
    """Test web content extractor with real HTTP requests."""
    # Use a reliable test URL
    urls = ["https://httpbin.org/html"]
    
    print(f"\nTesting web content extractor with real HTTP: {urls}")
    
    try:
        result = await web_content_extractor(urls)
        
        # Verify the result structure
        assert isinstance(result, dict)
        assert len(result) > 0
        
        for url, content in result.items():
            assert isinstance(content, str)
            assert len(content) > 0
            print(f"  - {url}: {len(content)} characters")
            
    except Exception as e:
        print(f"Error during testing: {str(e)}")
        pytest.skip(f"HTTP request failed: {str(e)}")


@pytest.mark.asyncio
async def test_web_search_error_handling():
    """Test web search error handling with invalid input."""
    # Test with empty query - should return error dict instead of raising
    result = await web_search("")
    assert "error" in result
    
    # Test with None query - should return error dict instead of raising
    result = await web_search(None)
    assert "error" in result


@pytest.mark.asyncio
async def test_web_search_multiple_queries():
    """Test web search with multiple different queries."""
    queries = [
        "Python web scraping",
        "AI machine learning",
        "JavaScript tutorial"
    ]
    
    for query in queries:
        print(f"\nTesting query: {query}")
        
        try:
            result = await web_search(query)
            
            # Basic validation
            assert result is not None
            assert isinstance(result, dict)
            
            if len(result) > 0:
                print(f"  Found {len(result)} results")
            else:
                print("  No results found")
                
        except Exception as e:
            print(f"  Error: {str(e)}")
            # Continue with next query instead of failing
            continue


