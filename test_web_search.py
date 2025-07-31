import asyncio
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the src directory to the path so we can import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from tools.web_search_tool import web_search

async def test_web_search():
    """Test the web search tool with a sample query."""
    
    # Test query
    query = "latest developments in artificial intelligence 2024"
    
    print(f"Testing web search tool with query: '{query}'")
    print("=" * 60)
    
    try:
        results = await web_search(query)
        
        print(f"Found {len(results)} results:")
        print()
        
        for i, (url, summary) in enumerate(results, 1):
            print(f"Result {i}:")
            print(f"URL: {url}")
            print(f"Summary: {summary[:500]}{'...' if len(summary) > 500 else ''}")
            print("-" * 60)
            print()
            
    except Exception as e:
        print(f"Error testing web search tool: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_web_search()) 