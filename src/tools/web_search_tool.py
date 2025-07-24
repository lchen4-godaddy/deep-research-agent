from typing import Dict, List
from ddgs import DDGS
import asyncio
import logging

from scraper.simple_scraper import scrape_urls_async

from agents import function_tool


def source_finder(query: str) -> List[str]:
    """
    Search the web for the most relevant URLs based on the query.
    """
    try:
        ddgs = DDGS()
        results = list(ddgs.text(query, max_results=5))
        
        urls = [r['href'] for r in results if r.get('href')]
        return urls
    except Exception as e:
        logging.error(f"Error in source_finder: {str(e)}")
        return []


async def web_content_extractor(urls: List[str]) -> Dict[str, str]:
    """
    Extract content from multiple URLs using Scrapy.
    
    Args:
        urls: List of URLs to extract content from
        
    Returns:
        Dictionary mapping URLs to their extracted content
    """
    if not urls:
        return {}
    
    try:
        # Use the Scrapy-based scraper
        scraped_content = await scrape_urls_async(urls)
        
        # Convert the scraped content to the expected format
        result = {}
        for url, content_data in scraped_content.items():
            if isinstance(content_data, dict):
                # Extract the main content from the scraped data
                content = content_data.get('content', '')
                title = content_data.get('title', '')
                
                # Combine title and content
                if title and content:
                    result[url] = f"Title: {title}\n\nContent: {content}"
                elif content:
                    result[url] = content
                else:
                    result[url] = "No content extracted"
            else:
                result[url] = str(content_data)
        
        return result
        
    except Exception as e:
        logging.error(f"Error in web_content_extractor: {str(e)}")
        return {url: f"Error extracting content: {str(e)}" for url in urls}

async def web_search(query: str) -> Dict[str, str]:
    """
    Search the web for information and extract content from relevant URLs.
    
    Args:
        query: The search query
        
    Returns:
        Dictionary mapping URLs to their extracted content
    """
    try:
        # Find relevant URLs
        urls = source_finder(query)
        
        if not urls:
            return {"error": "No URLs found for the query"}
        
        # Extract content from the URLs
        content = await web_content_extractor(urls)
        
        return content
        
    except Exception as e:
        logging.error(f"Error in web_search_tool: {str(e)}")
        return {"error": f"Error during web search: {str(e)}"}

@function_tool
async def web_search_tool(query: str) -> Dict[str, str]:
    """
    Search the web for information and extract content from relevant URLs.
    
    Args:
        query: The search query
        
    Returns:
        Dictionary mapping URLs to their extracted content
    """
    try:
        # Find relevant URLs
        urls = source_finder(query)
        
        if not urls:
            return {"error": "No URLs found for the query"}
        
        # Extract content from the URLs
        content = await web_content_extractor(urls)
        
        return content
        
    except Exception as e:
        logging.error(f"Error in web_search_tool: {str(e)}")
        return {"error": f"Error during web search: {str(e)}"}