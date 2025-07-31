#!/usr/bin/env python3
"""
Test script for the web scraper tool.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from bs4 import BeautifulSoup
import requests

from src.tools.web_scraper import WebScraper, scrape_url


class TestWebScraper:
    """Test cases for the WebScraper class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.scraper = WebScraper(timeout=5)
        self.test_url = "https://example.com"
        self.test_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Test Page</title>
        </head>
        <body>
            <header>Navigation</header>
            <main>
                <h1>Main Title</h1>
                <p>This is the first paragraph with some content.</p>
                <h2>Subtitle</h2>
                <p>This is the second paragraph with more content.</p>
                <div>
                    <p>This is a paragraph inside a div.</p>
                    <span>This is some span text.</span>
                </div>
            </main>
            <footer>Footer content</footer>
        </body>
        </html>
        """
    
    def test_init(self):
        """Test WebScraper initialization."""
        scraper = WebScraper(timeout=15)
        assert scraper.timeout == 15
        assert scraper.session is not None
        assert 'User-Agent' in scraper.session.headers
    
    def test_is_valid_url_valid(self):
        """Test URL validation with valid URLs."""
        valid_urls = [
            "https://example.com",
            "http://test.org/path",
            "https://subdomain.example.com/path?param=value#fragment"
        ]
        
        for url in valid_urls:
            assert self.scraper._is_valid_url(url) is True
    
    def test_is_valid_url_invalid(self):
        """Test URL validation with invalid URLs."""
        invalid_urls = [
            "not-a-url",
            "ftp://example.com",  # Unsupported scheme
            "example.com",  # Missing scheme
            "",
            None
        ]
        
        for url in invalid_urls:
            assert self.scraper._is_valid_url(url) is False
    
    def test_extract_main_content_with_main_tag(self):
        """Test main content extraction when main tag is present."""
        html = """
        <html>
        <body>
            <nav>Navigation</nav>
            <main>
                <h1>Main Content</h1>
                <p>This is the main content.</p>
            </main>
            <aside>Sidebar</aside>
        </body>
        </html>
        """
        soup = BeautifulSoup(html, 'html.parser')
        
        content = self.scraper._extract_main_content(soup)
        
        # Should contain main content but not nav or aside
        assert "Main Content" in content
        assert "This is the main content" in content
        assert "Navigation" not in content
        assert "Sidebar" not in content
    
    def test_extract_main_content_without_main_tag(self):
        """Test main content extraction when main tag is not present."""
        html = """
        <html>
        <body>
            <div class="content">
                <h1>Content</h1>
                <p>This is the content.</p>
            </div>
        </body>
        </html>
        """
        soup = BeautifulSoup(html, 'html.parser')
        
        content = self.scraper._extract_main_content(soup)
        
        # Should fall back to body content
        assert "Content" in content
        assert "This is the content" in content
    
    def test_format_content_with_headings_and_paragraphs(self):
        """Test content formatting with headings and paragraphs."""
        html = """
        <div>
            <h1>Title</h1>
            <p>First paragraph</p>
            <h2>Subtitle</h2>
            <p>Second paragraph</p>
        </div>
        """
        
        result = self.scraper._format_content(html)
        
        # Should have line breaks between sections
        assert "Title" in result
        assert "First paragraph" in result
        assert "Subtitle" in result
        assert "Second paragraph" in result
        
        # Check that line breaks are present
        lines = result.split('\n')
        assert len(lines) >= 4  # Should have multiple lines
    
    def test_should_add_line_break_headings(self):
        """Test line break logic for headings."""
        soup = BeautifulSoup("<h1>Title</h1>", 'html.parser')
        h1_element = soup.find('h1')
        
        assert self.scraper._should_add_line_break(h1_element) is True
    
    def test_should_add_line_break_paragraphs(self):
        """Test line break logic for paragraphs."""
        soup = BeautifulSoup("<p>Content</p>", 'html.parser')
        p_element = soup.find('p')
        
        assert self.scraper._should_add_line_break(p_element) is True
    
    def test_should_add_line_break_div_with_content(self):
        """Test line break logic for divs with content."""
        soup = BeautifulSoup("<div><p>Content</p></div>", 'html.parser')
        div_element = soup.find('div')
        
        assert self.scraper._should_add_line_break(div_element) is True
    
    def test_should_add_line_break_span(self):
        """Test line break logic for spans (should not add break)."""
        soup = BeautifulSoup("<span>Content</span>", 'html.parser')
        span_element = soup.find('span')
        
        assert self.scraper._should_add_line_break(span_element) is False
    
    @patch('requests.Session.get')
    def test_scrape_url_success(self, mock_get):
        """Test successful URL scraping."""
        # Mock the response
        mock_response = Mock()
        mock_response.content = self.test_html.encode()
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = self.scraper.scrape_url(self.test_url)
        
        assert result is not None
        assert "Main Title" in result
        assert "first paragraph" in result
        assert "Subtitle" in result
        assert "second paragraph" in result
    
    @patch('requests.Session.get')
    def test_scrape_url_request_exception(self, mock_get):
        """Test URL scraping with request exception."""
        mock_get.side_effect = requests.RequestException("Connection error")
        
        result = self.scraper.scrape_url(self.test_url)
        
        assert result is None
    
    @patch('requests.Session.get')
    def test_scrape_url_invalid_url(self, mock_get):
        """Test URL scraping with invalid URL."""
        result = self.scraper.scrape_url("not-a-url")
        
        assert result is None
        mock_get.assert_not_called()


class TestScrapeUrlFunction:
    """Test cases for the convenience scrape_url function."""
    
    @patch('src.tools.web_scraper.web_scraper.WebScraper')
    def test_scrape_url_function(self, mock_scraper_class):
        """Test the convenience scrape_url function."""
        # Mock the scraper instance
        mock_scraper = Mock()
        mock_scraper_class.return_value = mock_scraper
        mock_scraper.scrape_url.return_value = "Test content"
        
        result = scrape_url("https://example.com", timeout=15)
        
        # Verify the scraper was created with correct timeout
        mock_scraper_class.assert_called_once_with(timeout=15)
        
        # Verify scrape_url was called
        mock_scraper.scrape_url.assert_called_once_with("https://example.com")
        
        assert result == "Test content"


class TestWebScraperIntegration:
    """Integration tests for the web scraper."""
    
    @pytest.mark.integration
    def test_scrape_real_website(self):
        """Test scraping a real website (marked as integration test)."""
        scraper = WebScraper(timeout=10)
        
        # Use a reliable test website
        result = scraper.scrape_url("https://httpbin.org/html")
        
        # Should get some content
        assert result is not None
        assert len(result) > 0
        
        # Should contain some expected content from httpbin
        assert "Herman Melville" in result or "Moby Dick" in result
    
    @pytest.mark.integration
    def test_scrape_url_function_real_website(self):
        """Test the convenience function with a real website."""
        result = scrape_url("https://httpbin.org/html", timeout=10)
        
        assert result is not None
        assert len(result) > 0


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"]) 