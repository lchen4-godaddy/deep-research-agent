import requests
from bs4 import BeautifulSoup
import re
from typing import Optional, Tuple
from urllib.parse import urlparse
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WebScraper:
    """
    A web scraper that extracts main text content and titles from web pages
    and separates paragraphs/sections using HTML tags as indicators.
    """
    
    def __init__(self, timeout: int = 10):
        """
        Initialize the web scraper.
        
        Args:
            timeout: Request timeout in seconds
        """
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def scrape_url(self, url: str) -> Optional[Tuple[str, str]]:
        """
        Scrape the main text content and title from a URL.
        
        Args:
            url: The URL to scrape
            
        Returns:
            Tuple of (title, content) where content is extracted text with paragraphs/sections separated by line breaks,
            or None if scraping fails
        """
        try:
            # Validate URL
            if not self._is_valid_url(url):
                logger.error(f"Invalid URL: {url}")
                return None
            
            # Fetch the webpage
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract title
            title = self._extract_title(soup)
            
            # Extract main content
            content = self._extract_main_content(soup)
            
            if not content:
                logger.warning(f"No main content found for URL: {url}")
                return None
            
            # Clean and format the content
            formatted_content = self._format_content(content)
            
            return (title, formatted_content)
            
        except requests.RequestException as e:
            logger.error(f"Request failed for URL {url}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error scraping URL {url}: {e}")
            return None
    
    def _extract_title(self, soup: BeautifulSoup) -> str:
        """
        Extract the page title from the HTML soup.
        
        Args:
            soup: BeautifulSoup object of the HTML
            
        Returns:
            Extracted page title
        """
        # Try to get the title from the title tag
        title_tag = soup.find('title')
        if title_tag:
            title = title_tag.get_text(strip=True)
            if title:
                return title
        
        # Fallback: try to get title from h1 tag
        h1_tag = soup.find('h1')
        if h1_tag:
            title = h1_tag.get_text(strip=True)
            if title:
                return title
        
        # Fallback: try to get title from og:title meta tag
        og_title = soup.find('meta', property='og:title')
        if og_title and og_title.get('content'):
            return og_title.get('content')
        
        # Final fallback: return a generic title
        return "Untitled Page"
    
    def _is_valid_url(self, url: str) -> bool:
        """
        Validate if the provided string is a valid URL.
        
        Args:
            url: URL string to validate
            
        Returns:
            True if valid URL, False otherwise
        """
        try:
            result = urlparse(url)
            # Check for scheme and netloc, and ensure scheme is http or https
            return all([result.scheme, result.netloc]) and result.scheme in ['http', 'https']
        except Exception:
            return False
    
    def _extract_main_content(self, soup: BeautifulSoup) -> str:
        """
        Extract the main content from the HTML soup.
        
        Args:
            soup: BeautifulSoup object of the HTML
            
        Returns:
            Extracted text content
        """
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "header", "footer", "aside"]):
            script.decompose()
        
        # Try to find main content areas
        main_content = ""
        
        # Look for common main content selectors
        main_selectors = [
            'main',
            'article',
            '[role="main"]',
            '.main-content',
            '.content',
            '#content',
            '#main',
            '.post-content',
            '.entry-content'
        ]
        
        for selector in main_selectors:
            element = soup.select_one(selector)
            if element:
                main_content = str(element)
                break
        
        # If no main content found, use the body
        if not main_content:
            body = soup.find('body')
            if body:
                main_content = str(body)
            else:
                main_content = str(soup)
        
        return main_content
    
    def _format_content(self, html_content: str) -> str:
        """
        Format the HTML content by separating paragraphs/sections using HTML tags.
        
        Args:
            html_content: Raw HTML content
            
        Returns:
            Formatted text with line breaks separating sections
        """
        # Create a new soup object for parsing
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Get all text elements
        text_elements = []
        
        for element in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'div', 'span']):
            text = element.get_text(strip=True)
            if text:
                # Determine if this element should trigger a line break
                should_add_break = self._should_add_line_break(element)
                
                if should_add_break and text_elements:
                    text_elements.append('\n')
                
                text_elements.append(text)
        
        # Join all text elements
        result = ''.join(text_elements)
        
        # Clean up multiple line breaks
        result = re.sub(r'\n{3,}', '\n\n', result)
        
        return result.strip()
    
    def _should_add_line_break(self, element) -> bool:
        """
        Determine if a line break should be added before this element.
        
        Args:
            element: BeautifulSoup element
            
        Returns:
            True if line break should be added, False otherwise
        """
        # Always add line break for headings
        if element.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            return True
        
        # Add line break for paragraphs
        if element.name == 'p':
            return True
        
        # Add line break for divs that contain significant content
        if element.name == 'div':
            # Check if this div contains multiple paragraphs or headings
            has_paragraphs = element.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
            if has_paragraphs:
                return True
        
        return False


def scrape_url(url: str, timeout: int = 10) -> Optional[Tuple[str, str]]:
    """
    Convenience function to scrape a URL.
    
    Args:
        url: The URL to scrape
        timeout: Request timeout in seconds
        
    Returns:
        Tuple of (title, content) where content is extracted text with paragraphs/sections separated by line breaks,
        or None if scraping fails
    """
    scraper = WebScraper(timeout=timeout)
    return scraper.scrape_url(url)


if __name__ == "__main__":
    # Example usage
    test_url = "https://example.com"
    result = scrape_url(test_url)
    
    if result:
        title, content = result
        print(f"Title: {title}")
        print("Scraped content:")
        print(content)
    else:
        print("Failed to scrape content") 