"""
Chunked scraper that combines page scraping with text chunking.
"""

import asyncio
from typing import Dict, List, Optional
from .page_scraper import scrape_single_page
from .chunking import chunk_paragraphs, chunk_text


async def scrape_and_chunk_page(url: str, max_tokens: int = 512, 
                               model_name: str = "text-embedding-3-small") -> Dict[str, any]:
    """
    Scrape a page and return chunked content.
    
    Args:
        url: URL to scrape
        max_tokens: Maximum tokens per chunk
        model_name: Name of the OpenAI embedding model
        
    Returns:
        Dictionary with scraped and chunked content
    """
    # First scrape the page
    scraped_data = await scrape_single_page(url)
    
    if scraped_data['status'] != 'success':
        return scraped_data
    
    # Extract paragraphs and chunk them
    paragraphs = scraped_data.get('paragraphs', [])
    chunked_paragraphs = chunk_paragraphs(paragraphs, max_tokens, model_name)
    
    # Also chunk the full content
    content = scraped_data.get('content', '')
    chunked_content = chunk_text(content, max_tokens, model_name)
    
    # Add chunking information to the result
    result = scraped_data.copy()
    result.update({
        'chunked_paragraphs': chunked_paragraphs,
        'chunked_content': chunked_content,
        'chunk_count': len(chunked_paragraphs),
        'content_chunk_count': len(chunked_content),
        'max_tokens_per_chunk': max_tokens,
        'embedding_model': model_name
    })
    
    return result


async def scrape_and_chunk_multiple_pages(urls: List[str], max_tokens: int = 512,
                                        model_name: str = "text-embedding-3-small") -> Dict[str, any]:
    """
    Scrape multiple pages and return chunked content for each.
    
    Args:
        urls: List of URLs to scrape
        max_tokens: Maximum tokens per chunk
        model_name: Name of the OpenAI embedding model
        
    Returns:
        Dictionary mapping URLs to their chunked content
    """
    if not urls:
        return {}
    
    # Scrape all pages concurrently
    tasks = [scrape_and_chunk_page(url, max_tokens, model_name) for url in urls]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Combine results
    combined_results = {}
    for i, result in enumerate(results):
        url = urls[i]
        if isinstance(result, Exception):
            combined_results[url] = {
                'url': url,
                'status': 'error',
                'error': str(result),
                'chunked_paragraphs': [],
                'chunked_content': [],
                'chunk_count': 0,
                'content_chunk_count': 0
            }
        else:
            combined_results[url] = result
    
    return combined_results


def analyze_chunks(chunked_data: Dict[str, any]) -> Dict[str, any]:
    """
    Analyze chunked data to provide statistics and insights.
    
    Args:
        chunked_data: Data from scrape_and_chunk_page
        
    Returns:
        Analysis dictionary with statistics
    """
    if chunked_data['status'] != 'success':
        return {'error': 'No analysis possible for failed scrape'}
    
    chunked_paragraphs = chunked_data.get('chunked_paragraphs', [])
    chunked_content = chunked_data.get('chunked_content', [])
    
    # Calculate statistics
    total_chunks = len(chunked_paragraphs)
    total_content_chunks = len(chunked_content)
    
    chunk_lengths = [len(chunk) for chunk in chunked_paragraphs]
    content_chunk_lengths = [len(chunk) for chunk in chunked_content]
    
    analysis = {
        'url': chunked_data.get('url', ''),
        'total_paragraphs': chunked_data.get('paragraph_count', 0),
        'total_chunks': total_chunks,
        'total_content_chunks': total_content_chunks,
        'avg_chunk_length': sum(chunk_lengths) / len(chunk_lengths) if chunk_lengths else 0,
        'avg_content_chunk_length': sum(content_chunk_lengths) / len(content_chunk_lengths) if content_chunk_lengths else 0,
        'max_chunk_length': max(chunk_lengths) if chunk_lengths else 0,
        'min_chunk_length': min(chunk_lengths) if chunk_lengths else 0,
        'max_tokens_per_chunk': chunked_data.get('max_tokens_per_chunk', 0),
        'embedding_model': chunked_data.get('embedding_model', ''),
        'chunk_distribution': {
            'short_chunks': len([c for c in chunk_lengths if c < 100]),
            'medium_chunks': len([c for c in chunk_lengths if 100 <= c < 500]),
            'long_chunks': len([c for c in chunk_lengths if c >= 500])
        }
    }
    
    return analysis


async def scrape_with_analysis(url: str, max_tokens: int = 512,
                              model_name: str = "text-embedding-3-small") -> Dict[str, any]:
    """
    Scrape a page, chunk it, and provide analysis.
    
    Args:
        url: URL to scrape
        max_tokens: Maximum tokens per chunk
        model_name: Name of the OpenAI embedding model
        
    Returns:
        Dictionary with scraped content, chunks, and analysis
    """
    # Scrape and chunk
    chunked_data = await scrape_and_chunk_page(url, max_tokens, model_name)
    
    # Add analysis
    analysis = analyze_chunks(chunked_data)
    chunked_data['analysis'] = analysis
    
    return chunked_data 