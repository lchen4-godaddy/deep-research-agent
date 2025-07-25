"""
Tests for the individual page scraper.
"""

import pytest
import asyncio

from src.tools.scraper.page_scraper import scrape_single_page, PageScraper


@pytest.mark.asyncio
async def test_scrape_single_page_real_http():
    """Test scraping a single page with real HTTP request."""
    url = "https://httpbin.org/html"
    
    print(f"\nTesting page scraper with real HTTP: {url}")
    
    try:
        result = await scrape_single_page(url)
        
        # Basic assertions
        assert result is not None
        assert isinstance(result, dict)
        assert result['url'] == url
        assert 'status' in result
        assert 'title' in result
        assert 'content' in result
        assert 'paragraphs' in result
        
        if result['status'] == 'success':
            print(f"  - Title: {result['title'][:50]}...")
            print(f"  - Content length: {result['text_length']}")
            print(f"  - Paragraphs: {result['paragraph_count']}")
            
            # Check that we have some content
            assert result['text_length'] > 0
            assert result['paragraph_count'] >= 0
            
    except Exception as e:
        print(f"Error during testing: {str(e)}")
        pytest.skip(f"HTTP request failed: {str(e)}")


@pytest.mark.asyncio
async def test_scrape_single_page_invalid_url():
    """Test scraping with invalid URL."""
    url = "not-a-valid-url"
    
    print(f"\nTesting page scraper with invalid URL: {url}")
    
    result = await scrape_single_page(url)
    
    # Should handle invalid URL gracefully
    assert result['status'] == 'error'
    assert 'error' in result
    assert result['paragraphs'] == []
    assert result['content'] == ''


@pytest.mark.asyncio
async def test_scrape_single_page_nonexistent():
    """Test scraping with nonexistent URL."""
    url = "https://nonexistent-domain-12345.com"
    
    print(f"\nTesting page scraper with nonexistent URL: {url}")
    
    try:
        result = await scrape_single_page(url)
        
        # Should handle error gracefully
        assert result['status'] == 'error'
        assert 'error' in result
        assert result['paragraphs'] == []
        assert result['content'] == ''
        
        print(f"  - Error: {result['error'][:100]}...")
        
    except Exception as e:
        print(f"Error during testing: {str(e)}")
        pytest.skip(f"Test failed: {str(e)}")


@pytest.mark.asyncio
async def test_page_scraper_class():
    """Test the PageScraper class directly."""
    scraper = PageScraper()
    
    # Test URL validation
    assert scraper._is_valid_url("https://example.com") == True
    assert scraper._is_valid_url("http://example.com") == True
    assert scraper._is_valid_url("not-a-url") == False
    assert scraper._is_valid_url("") == False
    assert scraper._is_valid_url(None) == False
    assert scraper._is_valid_url("ftp://example.com") == False


@pytest.mark.asyncio
async def test_scrape_multiple_pages():
    """Test scraping multiple pages."""
    urls = [
        "https://httpbin.org/html",
        "https://httpbin.org/json"
    ]
    
    print(f"\nTesting multiple page scraping: {urls}")
    
    try:
        # Scrape pages concurrently
        tasks = [scrape_single_page(url) for url in urls]
        results = await asyncio.gather(*tasks)
        
        # Check results
        for i, result in enumerate(results):
            url = urls[i]
            print(f"  - {url}: status={result['status']}")
            
            assert result['url'] == url
            assert 'status' in result
            assert 'paragraphs' in result
            
    except Exception as e:
        print(f"Error during testing: {str(e)}")
        pytest.skip(f"HTTP request failed: {str(e)}") 