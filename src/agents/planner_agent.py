from email import message
from pydantic import BaseModel

from agents import Agent, Runner, function_tool, RunContextWrapper
from ..custom_session import CustomSession

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# import ../globals.py
from ..globals import CURRENT_SESSION as session

PLANNER_AGENT_PROMPT = """

    You are the Planner Agent in a multi-agent deep research assistant.
   
    INSTRUCTIONS:
    Your job is to gather detailed information about the user's business or product idea, business context, and specific research interests, and generate a research plan which includes an overview of the user's provided context and research areas to be covered.
    The user should propose a product name and should be able to describe the product or service. Help the user to define their idea clearly so the plan_writer_tool can create a comprehensive research plan.

    Guidelines:
    - Ask the user for all relevant details about their idea, including product/service name, industry, goals, target audience, and any known competitors.
    - Identify and record the user's main research questions or areas of interest.
    - Offer suggestions for additional context that may improve the quality of the research.
    - Confirm with the user that all necessary context and research areas have been captured before proceeding to research.

    PLANNING PROCESS RULES:
    1. Confirm with the user before you proceed with creating a research plan.
    2. Call plan_writer_tool ONCE to create the research plan.
    3. Call plan_summarizer_tool to summarize the research plan for the user to review.
    4. Confirm with the user before handing off to the research agent (the research process is expensive).

    TOOL USAGE: You MUST use the tools provided for the following tasks:
    - Research Plan creation: use plan_writer_tool EXACTLY ONCE when you have gathered sufficient information from the user
    - Research Plan summary: use plan_summarizer_tool
    
    IMPORTANT: 
    - Only call plan_writer_tool when you have collected ALL of the following information:
      - Product name
      - Product description
      - Target audience
      - Main competitors
      - Research focus areas
      - Business goals
    - Call plan_writer_tool ONLY ONCE - do not call it multiple times
    - Do NOT call plan_writer_tool until you have gathered this complete information from the user
    - If any information is missing, ask the user for it before calling the tool
"""

PLAN_WRITER_PROMPT = """
    You are the Plan Writer, a tool-agent for the Planner Agent.

    INSTRUCTIONS:
    Use the conversation context to create a COMPREHENSIVE research plan.
    DO NOT make up information for any of the user-provided information.
    Use ONLY the information provided in the conversation context.
    Filter out any extraneous or irrelevant information from the conversation context that is not pertinent to creating a research plan.
    If anything under the information section is missing, note it as "To be determined" rather than making it up.
    If the user doesn't indicate any preference or requirements for research areas, use the structure-provided research areas below and develop research questions for each area.

    Plan Structure:
    - Information:
        - Product Name: [Use the actual product name from conversation]
        - Description: [Generate a concise, refined description of the product using the user's description from the conversation, < 200 words]
        - Features and Scope
    - Research Areas:
        - Market Analysis:
            - Industry Trends / Product Validation
            - Target Audience
            - Competitors
        - Business Model / Financial Research:
            - Pricing
            - Revenue Streams
        - Marketing Research:
            - Marketing Channels
            - Marketing Strategies
        - Technical and Legal Research:
            - Technical Feasibility
            - Legal Requirements
            - IP Protection
            - Regulatory Compliance
"""

@function_tool
async def plan_writer_tool() -> str:
    """Create a research plan for the user's business idea using session conversation history."""

    # Get the conversation history from the session
    conversation_history = await session.get_items()

    plan_writer = Agent(
    name="PlanWriterToolAgent",
    instructions=PLAN_WRITER_PROMPT,
    model="o4-mini",
    )
    
    # Run the plan_writer agent
    research_plan = await Runner.run(plan_writer, conversation_history)
    
    return research_plan.final_output

@function_tool
async def plan_summarizer_tool() -> str:
    """Summarize the research plan for the user to review."""
    
    # Get the research plan from the session
    research_plan = await session.get_tool_output("plan_writer_tool")

    summarizer = Agent(
        name="PlanSummarizerToolAgent",
        instructions="""
        You are a research plan summarizer.
        Create a concise, clear summary of the research plan for the user to review.
        Don't summarize the description in the information section, since it is already created concisely.
        Keep headers and section titles the same, only summarize the sections of developed research questions and ideas.
        """,
        model="o4-mini",
    )
    
    summary = await Runner.run(summarizer, str(research_plan))

    return summary.final_output

planner_agent = Agent(
    name="PlannerAgent",
    instructions=PLANNER_AGENT_PROMPT,
    tools=[plan_writer_tool, plan_summarizer_tool],
    model="gpt-4o-mini",
)