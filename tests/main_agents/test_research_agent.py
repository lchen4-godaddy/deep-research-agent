#!/usr/bin/env python3
"""
Test script for the research_agent with a single research question to identify issues.
"""

import asyncio
import pytest
from unittest.mock import Mock, AsyncMock, patch
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from src.agent_memory import AGENT_MEMORY
from src.main_agents.research_agent import research_agent
from agents import Runner

async def test_research_agent_single_question():
    """Test the research_agent with a single research question to identify issues."""
    
    # Clear any existing data
    await AGENT_MEMORY.clear_research_plan()
    await AGENT_MEMORY.clear_research_dump()
    await AGENT_MEMORY.clear_report()
    
    # Create a simple test research plan with one question
    test_plan = """
    # Research Plan for Testing
    
    ## Information
    - Product Name: Test Research Product
    - Description: A simple test to identify research agent issues
    - Features & Scope: Basic functionality testing
    
    ## Research Areas
    
    ### Market Analysis
    - Sub-topics: Basic Market Research
    - Summary: Simple market analysis for testing
    - Research Question: What are the current trends in AI technology in 2024?
    """
    
    # Store the research plan in agent memory
    await AGENT_MEMORY.store_research_plan(test_plan)
    
    print("=" * 60)
    print("STARTING RESEARCH AGENT TEST")
    print("=" * 60)
    print(f"Test research plan: {test_plan}")
    print("-" * 60)
    
    try:
        # Test the research_agent
        print("🔍 Calling research_agent...")
        result = await Runner.run(research_agent, "Please conduct research based on the research plan.")
        
        print("✅ Research agent completed!")
        print(f"Final output: {result.final_output}")
        print("-" * 60)
        
        # Check what was stored in research dump
        all_research_dump = await AGENT_MEMORY.get_research_dump()
        print(f"Research dump entries: {len(all_research_dump)}")
        
        for question, entries in all_research_dump.items():
            print(f"\n📝 Research Question: {question}")
            print(f"📊 Number of sources: {len(entries)}")
            for i, ((title, url), summary) in enumerate(entries[:3]):  # Show first 3 entries
                print(f"  📄 Source {i+1}:")
                print(f"    Title: {title}")
                print(f"    URL: {url}")
                print(f"    Summary: {summary[:150]}...")  # Truncate long summaries
                print()
        
        # Check if report was generated
        report = await AGENT_MEMORY.get_report()
        print(f"📋 Report generated: {'Yes' if report else 'No'}")
        if report:
            print(f"📋 Report length: {len(report)} characters")
            print(f"📋 Report preview: {report[:300]}...")
        
        # Check agent state
        print(f"🔍 Report generated state: {AGENT_MEMORY.get_state('report_generated')}")
        
        print("\n" + "=" * 60)
        print("TEST ANALYSIS")
        print("=" * 60)
        
        # Analyze the results
        if len(all_research_dump) == 0:
            print("❌ ISSUE: No research data was collected")
            print("   - This suggests the research_tool failed or didn't run")
        elif len(all_research_dump) < 1:
            print("❌ ISSUE: Insufficient research data")
            print(f"   - Only {len(all_research_dump)} questions were researched")
        else:
            print("✅ Research data collection appears successful")
            
        if not report:
            print("❌ ISSUE: No report was generated")
            print("   - This suggests the report_writer_tool failed or didn't run")
        else:
            print("✅ Report generation appears successful")
            
        if not result.final_output:
            print("❌ ISSUE: Research agent didn't provide final output")
        else:
            print("✅ Research agent provided final output")
            
        print("\n🔍 POTENTIAL ISSUES TO INVESTIGATE:")
        print("1. Check if research_tool is being called")
        print("2. Check if report_writer_tool is being called")
        print("3. Check if tools are completing successfully")
        print("4. Check if agent is following the required workflow")
        
    except Exception as e:
        print(f"❌ ERROR during research agent test: {e}")
        import traceback
        traceback.print_exc()

async def test_research_agent_with_mock_tools():
    """Test the research_agent with mocked tools to isolate issues."""
    
    # Clear any existing data
    await AGENT_MEMORY.clear_research_plan()
    await AGENT_MEMORY.clear_research_dump()
    await AGENT_MEMORY.clear_report()
    
    # Create a simple test research plan
    test_plan = """
    # Research Plan for Mock Testing
    
    ## Information
    - Product Name: Mock Test Product
    - Description: Testing with mocked tools
    
    ## Research Areas
    
    ### Market Analysis
    - Research Question: What are the current trends in AI technology in 2024?
    """
    
    await AGENT_MEMORY.store_research_plan(test_plan)
    
    print("\n" + "=" * 60)
    print("TESTING WITH MOCKED TOOLS")
    print("=" * 60)
    
    # Mock the research_tool to return True
    with patch('src.tool_agents.research.research_tool.research_tool') as mock_research:
        mock_research.return_value = True
        
        # Mock the report_writer_tool to return a test report
        with patch('src.tool_agents.research.report_writer_tool.report_writer_tool') as mock_report:
            mock_report.return_value = "Test report content"
            
            try:
                result = await Runner.run(research_agent, "Please conduct research based on the research plan.")
                print(f"✅ Mock test completed: {result.final_output}")
            except Exception as e:
                print(f"❌ Mock test failed: {e}")
                import traceback
                traceback.print_exc()

if __name__ == "__main__":
    print("Running research agent tests...")
    asyncio.run(test_research_agent_single_question())
    asyncio.run(test_research_agent_with_mock_tools()) 