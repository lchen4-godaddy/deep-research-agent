#!/usr/bin/env python3
"""
Test script for the contextual_summary_tool with LLM call for human validation.
"""

import asyncio
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from src.tool_agents.research.contextual_summary_tool import contextual_summary_tool

async def test_contextual_summary_tool():
    """Test the contextual_summary_tool with LLM call for human validation."""
    
    # Test cases with different research questions and content
    test_cases = [
        {
            "question": "What are the latest developments in artificial intelligence in 2024?",
            "content": """
            Artificial Intelligence has seen remarkable progress in 2024, with significant breakthroughs in large language models, computer vision, and autonomous systems. 
            Companies like OpenAI, Google, and Microsoft have released increasingly sophisticated AI models that demonstrate improved reasoning capabilities and reduced hallucination rates. 
            The market for AI technologies is expected to reach $1.3 trillion by 2030, with generative AI alone projected to contribute $2.9 trillion annually to the global economy. 
            Key developments include the rise of multimodal AI systems that can process text, images, and audio simultaneously, as well as advances in AI safety and alignment research.
            """
        },
        {
            "question": "What is the market size for electric vehicles in the United States?",
            "content": """
            The electric vehicle market in the United States has experienced substantial growth in recent years. 
            In 2023, EV sales reached approximately 1.2 million units, representing about 7.6% of total vehicle sales. 
            Tesla continues to dominate the market with over 50% market share, followed by traditional automakers like Ford, GM, and Volkswagen. 
            The Biden administration's Inflation Reduction Act has provided significant incentives for EV adoption, including tax credits of up to $7,500 for qualifying vehicles. 
            Industry analysts project that EVs will account for 40% of new vehicle sales by 2030, driven by declining battery costs and expanding charging infrastructure.
            """
        },
        {
            "question": "What are the environmental impacts of renewable energy technologies?",
            "content": """
            Renewable energy technologies offer significant environmental benefits compared to fossil fuels, but they also present unique challenges. 
            Solar and wind power produce minimal greenhouse gas emissions during operation, helping to reduce carbon footprints and combat climate change. 
            However, the manufacturing of solar panels and wind turbines requires substantial amounts of rare earth elements and other materials, some of which are mined in environmentally sensitive areas. 
            Lifecycle assessments show that renewable energy systems typically have much lower environmental impacts than coal or natural gas power plants over their operational lifetime. 
            The International Energy Agency reports that renewable energy deployment has prevented approximately 2.1 billion tons of CO2 emissions annually.
            """
        }
    ]
    
    print("Starting contextual_summary_tool test...")
    print("-" * 50)
    
    try:
        for i, test_case in enumerate(test_cases, 1):
            question = test_case["question"]
            content = test_case["content"]
            
            print(f"\nTest {i}: {question}")
            print("-" * 30)
            print(f"Original content: {content[:200]}...")
            print()
            
            # Test the contextual_summary_tool
            result = await contextual_summary_tool(question, content)
            
            print(f"Contextual summary:")
            print(result)
            print(f"Summary length: {len(result)} characters")
            print()
        
        print("LLM Output for Human Validation:")
        print("The contextual_summary_tool has generated contextual summaries for each test case.")
        print("Please review the output above to validate the quality and relevance of the summaries.")
        
    except Exception as e:
        print(f"Error during contextual summarization: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_contextual_summary_tool()) 