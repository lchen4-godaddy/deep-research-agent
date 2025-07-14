from pydantic import BaseModel, Field
from typing import Dict, Any, List

from agents import Agent

PROMPT = """
    You are the Research Planner Agent.
    Your task is to take the user's business or product idea, business context, and requested research topics, then create a structured research plan.

    Guidelines:
    Create a comprehensive research plan that will be used to guide the research process in JSON format.
    Structure the plan with: business_idea, user_business_context, user_requested_research_areas, and research_plan_outline.
    The research_plan_outline should contain dynamically generated main topics (like 'Market Research', 'Business Model', etc.) with subtopics and specific research items under each to query the web for.
    Focus on actionable research that will help validate and launch the business idea.

"""

class ResearchPlan(BaseModel):
    business_idea: str
    """The main business or product idea"""
    user_business_context: str
    """Business context and background"""
    user_requested_research_areas: str
    """List of research areas requested by user"""
    research_plan_outline: str
    """Detailed research plan organized by dynamically generated main topics and subtopics"""

research_planner_agent = Agent(
    name="ResearchPlannerAgent",
    instructions=PROMPT,
    model="gpt-4o",
    output_type=ResearchPlan,
)