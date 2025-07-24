import asyncio
import logging
from typing import Dict, List, Any
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse


class SimpleWebScraper:
    """
    A simple web scraper using requests and BeautifulSoup.
    """
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; ResearchBot/1.0)'
        })
        self.logger = logging.getLogger(__name__)
    
    async def scrape_urls(self, urls: List[str]) -> Dict[str, Any]:
        """
        Scrape content from a list of URLs.
        
        Args:
            urls: List of URLs to scrape
            
        Returns:
            Dictionary mapping URLs to their extracted content
        """
        if not urls:
            return {}
        
        # Filter out invalid URLs
        valid_urls = [url for url in urls if self._is_valid_url(url)]
        
        if not valid_urls:
            self.logger.warning("No valid URLs provided for scraping")
            return {}
        
        self.logger.info(f"Starting to scrape {len(valid_urls)} URLs")
        
        results = {}
        
        for url in valid_urls:
            try:
                content = await self._scrape_single_url(url)
                results[url] = content
            except Exception as e:
                self.logger.error(f"Error scraping {url}: {str(e)}")
                results[url] = {
                    'title': '',
                    'content': f"Error extracting content: {str(e)}",
                    'text_length': 0,
                    'status': 'error'
                }
        
        self.logger.info(f"Successfully scraped {len(results)} URLs")
        return results
    
    def _is_valid_url(self, url: str) -> bool:
        """Check if a URL is valid for scraping."""
        if not url or not isinstance(url, str):
            return False
        
        # Basic URL validation
        if not url.startswith(('http://', 'https://')):
            return False
        
        # Skip certain file types
        skip_extensions = ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx']
        if any(url.lower().endswith(ext) for ext in skip_extensions):
            return False
        
        return True
    
    async def _scrape_single_url(self, url: str) -> Dict[str, Any]:
        """
        Scrape a single URL and extract content.
        
        Args:
            url: URL to scrape
            
        Returns:
            Dictionary with extracted content
        """
        # Use asyncio to run the blocking request in a thread pool
        loop = asyncio.get_event_loop()
        
        try:
            # Make the request
            response = await loop.run_in_executor(
                None, 
                lambda: self.session.get(url, timeout=10)
            )
            
            if response.status_code != 200:
                return {
                    'title': '',
                    'content': f"HTTP {response.status_code}: {response.reason}",
                    'text_length': 0,
                    'status': response.status_code
                }
            
            # Parse the HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract title
            title = self._extract_title(soup)
            
            # Extract content
            content = self._extract_content(soup)
            
            return {
                'title': title,
                'content': content,
                'text_length': len(content),
                'status': response.status_code
            }
            
        except Exception as e:
            self.logger.error(f"Error scraping {url}: {str(e)}")
            return {
                'title': '',
                'content': f"Error extracting content: {str(e)}",
                'text_length': 0,
                'status': 'error'
            }
    
    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extract the page title."""
        title = soup.find('title')
        if title:
            return title.get_text().strip()
        
        # Try h1 as fallback
        h1 = soup.find('h1')
        if h1:
            return h1.get_text().strip()
        
        return ''
    
    def _extract_content(self, soup: BeautifulSoup) -> str:
        """Extract main content from the page."""
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Extract text from various content areas
        content_selectors = [
            'article',
            'main',
            '.content',
            '.post-content',
            '.entry-content',
            '.article-content',
            '#content',
            '#main',
            'body'
        ]
        
        content_parts = []
        
        for selector in content_selectors:
            elements = soup.select(selector)
            for element in elements:
                # Get text from paragraphs, headings, and lists
                text_elements = element.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'div'])
                for text_elem in text_elements:
                    text = text_elem.get_text()
                    if text and len(text.strip()) > 20:  # Only keep substantial text
                        content_parts.append(text.strip())
        
        # If no content found with specific selectors, get all text
        if not content_parts:
            text = soup.get_text()
            content_parts = [t.strip() for t in text.split('\n') if t.strip() and len(t.strip()) > 10]
        
        # Clean and join content
        content = ' '.join(content_parts)
        
        # Clean up whitespace and normalize
        content = re.sub(r'\s+', ' ', content)
        content = content.strip()
        
        # Limit content length to avoid memory issues
        if len(content) > 10000:
            content = content[:10000] + "..."
        
        return content


# Global scraper instance
_scraper = None


def get_scraper() -> SimpleWebScraper:
    """Get the global scraper instance."""
    global _scraper
    if _scraper is None:
        _scraper = SimpleWebScraper()
    return _scraper


async def scrape_urls_async(urls: List[str]) -> Dict[str, Any]:
    """
    Async function to scrape URLs and return content.
    
    Args:
        urls: List of URLs to scrape
        
    Returns:
        Dictionary mapping URLs to their extracted content
    """
    scraper = get_scraper()
    return await scraper.scrape_urls(urls) 