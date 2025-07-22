from agents import Agent, Runner, function_tool

from ....globals import CURRENT_SESSION as session

SEARCH_PLANNER_PROMPT = """
    You are the Search Plan Tool.
    Given a research plan as input, create or modify an existing web search plan for the user's business or product idea.

    WebSearchPlan structure:
    - searches: list of WebSearchItem objects

    WebSearchItem structure:
    - reason: Your reasoning for why this search is important to the query
    - query: The search term to use for the web search

    IMPORTANT: If a search plan already exists and modifications are requested, use the current search plan as a template and modify the existing search plan. 
    Only modify the contents that the user requests. Do not create a new search plan from scratch, and do not modify fields which are not explicitly requested.
    """

@function_tool
async def search_plan_tool() -> str:
    """Generate a web search plan for the user's business idea using session context."""

    search_planner = Agent(
    name="SearchPlannerToolAgent",
    instructions=SEARCH_PLANNER_PROMPT,
    model="o4-mini",
    )

    # Get the research plan from the session
    research_plan = await session.get_tool_output("plan_writer_tool")

    # Run the search_plan agent
    search_plan = await Runner.run(search_planner, research_plan)
    
    return search_plan.final_output
    
