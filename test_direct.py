#!/usr/bin/env python3
"""
Direct test of the researcher_tool.
"""

import asyncio
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

async def test_direct():
    """Test the researcher_tool directly."""
    
    try:
        # Import the tool
        from src.tools.researcher_tool import researcher_tool
        print("✅ Successfully imported researcher_tool")
        
        # Test calling it
        test_question = "What are the latest developments in artificial intelligence in 2024?"
        print(f"Testing with question: {test_question}")
        
        result = await researcher_tool(test_question)
        print(f"✅ researcher_tool returned: {result}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_direct()) 