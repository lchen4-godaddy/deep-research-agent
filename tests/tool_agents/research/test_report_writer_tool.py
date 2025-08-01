#!/usr/bin/env python3
"""
Test script for the report_writer_tool with LLM call for human validation.
"""

import asyncio
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from src.agent_memory import AGENT_MEMORY
from src.tool_agents.research.report_writer_tool import report_writer_tool

async def test_report_writer_tool():
    """Test the report_writer_tool with LLM call for human validation."""
    
    # Clear any existing data
    await AGENT_MEMORY.clear_research_plan()
    await AGENT_MEMORY.clear_research_dump()
    
    # Create a test research plan
    test_plan = """
    # Research Plan for AI-Powered Research Assistant
    
    ## Information
    - Product Name: AI-Powered Research Assistant
    - Description: An AI tool that helps researchers and students conduct comprehensive research
    - Features & Scope: Web search, summarization, citation management
    
    ## Research Areas
    
    ### Market Analysis
    - Sub-topics: Industry Trends, Target Audience, Competitors
    - Summary: Explore the AI research tools market and identify opportunities
    - Research Question: What is the market size for AI-powered research tools?
    
    ### Business Model & Financial Research
    - Sub-topics: Pricing, Revenue Streams, Market Size
    - Summary: Analyze the business potential of AI research tools
    - Research Question: What are the typical pricing strategies for AI research tools?
    """
    
    # Create test research data
    test_research_data = {
        "What is the market size for AI-powered research tools?": [
            (("AI Research Tools Market Report 2024", "https://example.com/market-report"), 
             "The global AI research tools market is valued at $2.1 billion in 2024 and is expected to grow at a CAGR of 15.3% through 2030. Key drivers include increasing demand for automated research processes and the rise of AI-powered academic tools."),
            (("Top AI Research Platforms", "https://example.com/ai-platforms"), 
             "Leading AI research platforms include tools like ChatGPT, Claude, and specialized research assistants. The market is segmented into academic, corporate, and individual researcher segments, with academic institutions being the largest adopters.")
        ],
        "What are the typical pricing strategies for AI research tools?": [
            (("AI Tool Pricing Analysis", "https://example.com/pricing-analysis"), 
             "AI research tools typically use subscription-based pricing models, with monthly fees ranging from $10 to $500 depending on features and usage limits. Enterprise solutions often cost $1000+ per month with custom pricing for large organizations."),
            (("Freemium Models in AI Tools", "https://example.com/freemium-models"), 
             "Many AI research tools adopt freemium models, offering basic features for free while charging for advanced capabilities. This approach helps with user acquisition and allows for gradual monetization of power users.")
        ]
    }
    
    # Store the research plan and data in agent memory
    await AGENT_MEMORY.store_research_plan(test_plan)
    
    # Store research data
    for question, entries in test_research_data.items():
        for (title, url), summary in entries:
            await AGENT_MEMORY.store_in_research_dump(question, (title, url), summary)
    
    print("Starting report_writer_tool test...")
    print(f"Test research plan: {test_plan}")
    print(f"Test research data: {len(test_research_data)} questions with research results")
    print("-" * 50)
    
    try:
        # Test the report_writer_tool
        result = await report_writer_tool()
        
        print("Report writer tool completed!")
        print(f"Result: {result}")
        print("-" * 50)
        
        print("Generated Research Report:")
        print("=" * 50)
        print(result)
        print("=" * 50)
        
        print("\nLLM Output for Human Validation:")
        print("The report_writer_tool has generated a comprehensive research report based on the provided plan and data.")
        print("Please review the output above to validate the quality, structure, and completeness of the report.")
        
    except Exception as e:
        print(f"Error during report writing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_report_writer_tool()) 