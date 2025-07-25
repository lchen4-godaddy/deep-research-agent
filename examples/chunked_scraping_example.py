#!/usr/bin/env python3
"""
Example script demonstrating chunked scraping functionality.
"""

import asyncio
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.tools.scraper.page_scraper import scrape_single_page
from src.tools.scraper.chunking import chunk_paragraphs, chunk_text
from src.tools.scraper.chunked_scraper import scrape_and_chunk_page, scrape_with_analysis


async def example_basic_scraping():
    """Example of basic page scraping."""
    print("=== Basic Page Scraping ===")
    
    url = "https://httpbin.org/html"
    result = await scrape_single_page(url)
    
    print(f"URL: {result['url']}")
    print(f"Status: {result['status']}")
    print(f"Title: {result['title'][:100]}...")
    print(f"Content length: {result['text_length']}")
    print(f"Paragraphs: {result['paragraph_count']}")
    
    if result['paragraphs']:
        print(f"First paragraph: {result['paragraphs'][0][:100]}...")


async def example_chunking():
    """Example of text chunking."""
    print("\n=== Text Chunking ===")
    
    # Sample paragraphs
    paragraphs = [
        "This is the first paragraph with some content about web scraping.",
        "This is the second paragraph that discusses different techniques.",
        "This is the third paragraph that is quite long and contains more information about various topics including BeautifulSoup, Scrapy, and other tools.",
        "Short paragraph about Python.",
        "Another short one about programming."
    ]
    
    # Chunk the paragraphs
    chunks = chunk_paragraphs(paragraphs, max_tokens=100)
    
    print(f"Original paragraphs: {len(paragraphs)}")
    print(f"Resulting chunks: {len(chunks)}")
    
    for i, chunk in enumerate(chunks):
        print(f"Chunk {i+1}: {len(chunk)} characters")
        print(f"  Content: {chunk[:100]}...")


async def example_chunked_scraping():
    """Example of combined scraping and chunking."""
    print("\n=== Chunked Scraping ===")
    
    url = "https://httpbin.org/html"
    result = await scrape_and_chunk_page(url, max_tokens=200)
    
    print(f"URL: {result['url']}")
    print(f"Status: {result['status']}")
    print(f"Original paragraphs: {result['paragraph_count']}")
    print(f"Chunked paragraphs: {result['chunk_count']}")
    print(f"Content chunks: {result['content_chunk_count']}")
    
    if result['chunked_paragraphs']:
        print(f"First chunk: {result['chunked_paragraphs'][0][:100]}...")


async def example_with_analysis():
    """Example of scraping with analysis."""
    print("\n=== Scraping with Analysis ===")
    
    url = "https://httpbin.org/html"
    result = await scrape_with_analysis(url, max_tokens=200)
    
    if result['status'] == 'success':
        analysis = result['analysis']
        print(f"URL: {analysis['url']}")
        print(f"Total paragraphs: {analysis['total_paragraphs']}")
        print(f"Total chunks: {analysis['total_chunks']}")
        print(f"Average chunk length: {analysis['avg_chunk_length']:.1f}")
        print(f"Chunk distribution:")
        print(f"  - Short chunks: {analysis['chunk_distribution']['short_chunks']}")
        print(f"  - Medium chunks: {analysis['chunk_distribution']['medium_chunks']}")
        print(f"  - Long chunks: {analysis['chunk_distribution']['long_chunks']}")


async def example_multiple_pages():
    """Example of scraping multiple pages."""
    print("\n=== Multiple Page Scraping ===")
    
    from src.tools.scraper.chunked_scraper import scrape_and_chunk_multiple_pages
    
    urls = [
        "https://httpbin.org/html",
        "https://httpbin.org/json"
    ]
    
    results = await scrape_and_chunk_multiple_pages(urls, max_tokens=200)
    
    for url, result in results.items():
        print(f"\nURL: {url}")
        print(f"Status: {result['status']}")
        if result['status'] == 'success':
            print(f"Chunks: {result['chunk_count']}")
            print(f"Content chunks: {result['content_chunk_count']}")


async def main():
    """Run all examples."""
    print("Chunked Scraping Examples")
    print("=" * 50)
    
    try:
        await example_basic_scraping()
        await example_chunking()
        await example_chunked_scraping()
        await example_with_analysis()
        await example_multiple_pages()
        
        print("\n" + "=" * 50)
        print("All examples completed successfully!")
        
    except Exception as e:
        print(f"Error running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main()) 