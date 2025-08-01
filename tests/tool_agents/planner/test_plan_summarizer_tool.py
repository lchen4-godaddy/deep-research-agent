#!/usr/bin/env python3
"""
Test script for the plan_summarizer_tool with LLM call for human validation.
"""

import asyncio
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from src.agent_memory import AGENT_MEMORY
from src.tool_agents.planner.plan_summarizer_tool import plan_summarizer_tool

async def test_plan_summarizer_tool():
    """Test the plan_summarizer_tool with LLM call for human validation."""
    
    # Clear any existing data
    await AGENT_MEMORY.clear_research_plan()
    
    # Create a test research plan
    test_plan = """
    # Research Plan for Organic Coffee Business
    
    ## Information
    - Product Name: Organic Coffee Beans Online Store
    - Description: An online business selling premium organic coffee beans to health-conscious consumers
    - Features & Scope: E-commerce platform, organic certification, direct-to-consumer model
    
    ## Research Areas
    
    ### Market Analysis
    - Sub-topics: Industry Trends, Target Audience, Competitors
    - Summary: Explore the organic coffee market, identify target demographics, and analyze competition
    - Research Question: What is the current market size and growth potential for organic coffee in the US?
    
    ### Business Model & Financial Research
    - Sub-topics: Pricing, Revenue Streams, Cost Structure
    - Summary: Analyze pricing strategies and revenue models for online coffee businesses
    - Research Question: What are the typical pricing strategies and profit margins for online organic coffee retailers?
    
    ### Marketing Research
    - Sub-topics: Digital Marketing Channels, Brand Positioning, Customer Acquisition
    - Summary: Research effective marketing strategies for organic food products online
    - Research Question: What are the most effective digital marketing channels for reaching health-conscious coffee consumers?
    
    ### Technical & Legal Research
    - Sub-topics: E-commerce Platform, Food Safety Regulations, Organic Certification
    - Summary: Understand technical requirements and legal compliance for online food sales
    - Research Question: What are the legal requirements and certifications needed to sell organic coffee online in the US?
    """
    
    # Store the research plan in agent memory
    await AGENT_MEMORY.store_research_plan(test_plan)
    
    print("Starting plan_summarizer_tool test...")
    print(f"Original research plan: {test_plan}")
    print("-" * 50)
    
    try:
        # Test the plan_summarizer_tool
        result = await plan_summarizer_tool()
        
        print("Plan summarizer tool completed!")
        print(f"Result: {result}")
        print("-" * 50)
        
        print("LLM Output for Human Validation:")
        print("The plan_summarizer_tool has generated a summary of the research plan.")
        print("Please review the output above to validate the quality and clarity of the summary.")
        
    except Exception as e:
        print(f"Error during plan summarization: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_plan_summarizer_tool()) 