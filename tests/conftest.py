"""
Pytest configuration file for the deep-research-agent project.

This file sets up the Python path so that all test files can import from the src directory
without needing to manually manipulate sys.path in each test file.
"""

import sys
import os
from pathlib import Path
import pytest
from unittest.mock import Mock, AsyncMock

# Get the project root directory (parent of tests directory)
project_root = Path(__file__).parent.parent

# Add the project root to the Python path so we can import with 'src.' prefix
# This matches how the project is designed to be run (python -m src.main)
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))


# Test data constants
TEST_URLS = [
    "https://www.python.org",
    "https://docs.python.org/3/tutorial/",
    "https://scrapy.org/"
]

TEST_SEARCH_QUERIES = [
    "Python web scraping tutorial",
    "AI agents research",
    "Machine learning basics"
]

TEST_SCRAPED_CONTENT = {
    "https://www.python.org": {
        "title": "Welcome to Python.org",
        "content": "Python is a programming language that lets you work quickly and integrate systems more effectively.",
        "status": "success",
        "text_length": 150
    },
    "https://docs.python.org/3/tutorial/": {
        "title": "The Python Tutorial",
        "content": "Python is an easy to learn, powerful programming language.",
        "status": "success", 
        "text_length": 120
    }
}


@pytest.fixture
def mock_web_search_response():
    """Mock response for web search tool."""
    return {
        "https://example.com/1": "This is test content from example.com about Python web scraping.",
        "https://example.com/2": "Another test page with information about AI and machine learning.",
        "https://example.com/3": "Third test page with web development tutorials."
    }


@pytest.fixture
def mock_scraper_response():
    """Mock response for web scraper."""
    return {
        "https://example.com/1": {
            "title": "Python Web Scraping Tutorial",
            "content": "Learn how to scrape websites using Python and BeautifulSoup.",
            "status": "success",
            "text_length": 85
        },
        "https://example.com/2": {
            "title": "AI and Machine Learning Guide",
            "content": "Comprehensive guide to artificial intelligence and machine learning concepts.",
            "status": "success",
            "text_length": 95
        }
    }


@pytest.fixture
def mock_agent_response():
    """Mock response from an AI agent."""
    return {
        "summary": "This is a test summary of the research findings.",
        "key_points": ["Point 1", "Point 2", "Point 3"],
        "recommendations": ["Recommendation 1", "Recommendation 2"]
    }


@pytest.fixture
def mock_session():
    """Mock session object for testing."""
    session = Mock()
    session.data = {
        "research_query": "test query",
        "search_results": mock_web_search_response(),
        "scraped_content": mock_scraper_response(),
        "agent_responses": [mock_agent_response()]
    }
    session.add_data = Mock()
    session.get_data = Mock(return_value=session.data)
    return session


@pytest.fixture
def mock_openai_client():
    """Mock OpenAI client for testing."""
    client = Mock()
    client.chat.completions.create = AsyncMock()
    return client


@pytest.fixture
def sample_user_context():
    """Sample user context for testing."""
    return {
        "query": "Research the latest developments in AI agents",
        "requirements": "Need a comprehensive report with recent developments",
        "format": "detailed analysis"
    } 