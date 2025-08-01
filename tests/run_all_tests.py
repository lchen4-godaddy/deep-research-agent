#!/usr/bin/env python3
"""
Comprehensive test runner for all tool_agents and tools tests.
"""

import asyncio
import sys
import os
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

def run_test_module(module_path, description):
    """Run a test module and return success status."""
    print(f"\n{'='*60}")
    print(f"Running {description}")
    print(f"{'='*60}")
    
    try:
        # Import and run the test module
        module_name = module_path.replace('/', '.').replace('.py', '')
        module = __import__(module_name, fromlist=[''])
        
        # Find the main test function
        test_functions = [name for name in dir(module) if name.startswith('test_') and callable(getattr(module, name))]
        
        if test_functions:
            # Run the first test function found
            test_func = getattr(module, test_functions[0])
            if asyncio.iscoroutinefunction(test_func):
                asyncio.run(test_func())
            else:
                test_func()
            print(f"✅ {description} completed successfully")
            return True
        else:
            print(f"❌ No test functions found in {module_path}")
            return False
            
    except Exception as e:
        print(f"❌ Error running {description}: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Run all tests with options."""
    
    # Test modules to run
    test_modules = [
        # Tool Agents - Planner
        ("tests.tool_agents.planner.test_plan_writer_tool", "Plan Writer Tool"),
        ("tests.tool_agents.planner.test_plan_summarizer_tool", "Plan Summarizer Tool"),
        
        # Tool Agents - Research
        ("tests.tool_agents.research.test_research_tool", "Research Tool"),
        ("tests.tool_agents.research.test_query_writer_tool", "Query Writer Tool"),
        ("tests.tool_agents.research.test_contextual_summary_tool", "Contextual Summary Tool"),
        ("tests.tool_agents.research.test_report_writer_tool", "Report Writer Tool"),
        
        # Tools
        ("tests.tools.test_researcher", "Researcher Tool"),
        ("tests.tools.test_web_search_tool", "Web Search Tool"),
        ("tests.tools.web_scraper.test_web_scraper", "Web Scraper Tool"),
    ]
    
    print("🧪 Deep Research Agent - Comprehensive Test Suite")
    print("=" * 60)
    
    # Check if specific test is requested
    if len(sys.argv) > 1:
        test_name = sys.argv[1].lower()
        filtered_modules = [
            (module, desc) for module, desc in test_modules 
            if test_name in desc.lower() or test_name in module.lower()
        ]
        
        if filtered_modules:
            test_modules = filtered_modules
            print(f"Running tests matching: {test_name}")
        else:
            print(f"No tests found matching: {test_name}")
            print("Available tests:")
            for module, desc in test_modules:
                print(f"  - {desc} ({module})")
            return
    
    # Run all tests
    results = []
    for module_path, description in test_modules:
        success = run_test_module(module_path, description)
        results.append((description, success))
    
    # Summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print(f"{'='*60}")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for description, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {description}")
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests completed successfully!")
    else:
        print("⚠️  Some tests failed. Please review the output above.")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main()) 