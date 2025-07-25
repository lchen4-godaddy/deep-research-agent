"""
Individual page scraper for extracting content from single web pages.
"""

import asyncio
import logging
from typing import Dict, List, Optional
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse


class PageScraper:
    """
    A focused scraper for individual web pages with enhanced content extraction.
    """
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; ResearchBot/1.0)'
        })
        self.logger = logging.getLogger(__name__)
    
    async def scrape_page(self, url: str) -> Dict[str, any]:
        """
        Scrape a single web page and extract structured content.
        
        Args:
            url: URL to scrape
            
        Returns:
            Dictionary with extracted content including paragraphs
        """
        if not self._is_valid_url(url):
            return {
                'url': url,
                'title': '',
                'content': '',
                'paragraphs': [],
                'status': 'error',
                'error': 'Invalid URL'
            }
        
        try:
            # Use asyncio to run the blocking request in a thread pool
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None, 
                lambda: self.session.get(url, timeout=10)
            )
            
            if response.status_code != 200:
                return {
                    'url': url,
                    'title': '',
                    'content': '',
                    'paragraphs': [],
                    'status': 'error',
                    'error': f'HTTP {response.status_code}'
                }
            
            # Parse the HTML using lxml for better performance
            soup = BeautifulSoup(response.text, 'lxml')
            
            # Extract content
            title = self._extract_title(soup)
            content = self._extract_content(soup)
            paragraphs = self._extract_paragraphs(soup)
            
            return {
                'url': url,
                'title': title,
                'content': content,
                'paragraphs': paragraphs,
                'status': 'success',
                'text_length': len(content),
                'paragraph_count': len(paragraphs)
            }
            
        except Exception as e:
            self.logger.error(f"Error scraping {url}: {str(e)}")
            return {
                'url': url,
                'title': '',
                'content': '',
                'paragraphs': [],
                'status': 'error',
                'error': str(e)
            }
    
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
        # Remove non-content tags
        for tag in soup(['script', 'style', 'header', 'footer', 'nav', 'aside', 'meta', 'link']):
            tag.decompose()
        
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
        import re
        content = re.sub(r'\s+', ' ', content)
        content = content.strip()
        
        # Limit content length to avoid memory issues
        if len(content) > 10000:
            content = content[:10000] + "..."
        
        return content
    
    def _extract_paragraphs(self, soup: BeautifulSoup) -> List[str]:
        """Extract paragraphs from the page."""
        # Remove non-content tags
        for tag in soup(['script', 'style', 'header', 'footer', 'nav', 'aside']):
            tag.decompose()
        
        # Extract paragraphs
        paragraphs = []
        for p in soup.find_all('p'):
            text = p.get_text().strip()
            if text and len(text) > 20:  # Only keep substantial paragraphs
                paragraphs.append(text)
        
        return paragraphs


# Global scraper instance
_page_scraper = None


def get_page_scraper() -> PageScraper:
    """Get the global page scraper instance."""
    global _page_scraper
    if _page_scraper is None:
        _page_scraper = PageScraper()
    return _page_scraper


async def scrape_single_page(url: str) -> Dict[str, any]:
    """
    Async function to scrape a single page and return structured content.
    
    Args:
        url: URL to scrape
        
    Returns:
        Dictionary with extracted content including paragraphs
    """
    scraper = get_page_scraper()
    return await scraper.scrape_page(url) 