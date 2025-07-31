from typing import Dict, List, Tuple
from ddgs import DDGS
import asyncio
import logging

from src.tools.web_scraper.web_scraper import scrape_url
from src.tool_agents.research.contextual_summary_tool import contextual_summary_tool

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

async def web_search(query: str) -> List[Tuple[str, str]]:
    """
    Search the web for the most relevant URLs based on the query and return summaries.
    """
    urls = source_finder(query)
    results = []
    
    for url in urls:
        content = scrape_url(url)
        if content:
            try:
                summary = await contextual_summary_tool(query, content)
                results.append((url, summary))
            except Exception as e:
                logging.error(f"Error summarizing content for {url}: {str(e)}")
                # Fallback to original content if summarization fails
                results.append((url, content))
        else:
            logging.warning(f"Failed to scrape content from {url}")
    
    return results

@function_tool
async def web_search_tool(query: str) -> List[Tuple[str, str]]:
    """
    Function tool wrapper for web search functionality.
    Search the web for the most relevant URLs based on the query and return summaries.
    
    Args:
        query: str - the search query to use
        
    Returns:
        List of tuples containing (URL, summary) pairs
    """
    return await web_search(query)