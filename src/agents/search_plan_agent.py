from pydantic import BaseModel

from agents import Agent, Runner, function_tool, SQLiteSession, RunContextWrapper
from ..custom_session import CustomSession

SEARCH_PLAN_AGENT_PROMPT = """
    You are the Search Plan Agent in a multi-agent deep research assistant.
    Your job is to finalize the web search plan with the user, ensuring it aligns with their research objectives and interests.

    Guidelines:
    - Present the current web search plan, if available, to the user for confirmation and adjustments.
    - If no search plan exists, use search_plan_tool to generate one, then review it with the user.
    - Each item in the search plan should include a reason and a query. Work with the user to verify or modify these.
    - Encourage the user to add, remove, or refine search items as needed.
    - Confirm with the user that the finalized search plan fully covers their research needs before advancing.

    IMPORTANT: You MUST use the search_plan_tool to create a structured web search plan. Do not manually create the search plan - use the tool.
    IMPORTANT RULES:
    1. Only use the search_plan_tool once you have gotten permission from the user to proceed with a search plan or modify the existing one.
    2. If the user asks to "see" or "get" the search plan, retrieve it from the session data - DO NOT call the tool again.
      a. You may only format the search plan in a way that is easy to read and understand. Do not summarize or add any additional information.
    Your objective is to ensure all essential background information is gathered and validated by the user before moving to researching.

"""

SEARCH_PLAN_SUBAGENT_PROMPT = """
    You are the Search Plan Sub-Agent.
    Given the session context, create or modify an existing web search plan for the user's business or product idea.

    WebSearchPlan structure:
    - searches: list[WebSearchItem] (e.g. reason: "To find out about the latest trends in the industry", query: "latest trends in the industry")

    WebSearchItem structure:
    - reason: str (e.g. "To find out about the latest trends in the industry")
    - query: str (e.g. "latest trends in the industry")

    IMPORTANT: If a search plan already exists and modifications are requested, use the current search plan as a template and modify the existing search plan. Only modify the contents that the user requests. Do not create a new search plan from scratch, and do not modify fields which are not explicitly requested.

"""

class WebSearchItem(BaseModel):
    reason: str
    "Your reasoning for why this search is important to the query."

    query: str
    "The search term to use for the web search."


class WebSearchPlan(BaseModel):
    searches: list[WebSearchItem]
    """A list of web searches to perform to best answer the query."""


search_plan_subagent = Agent(
    name="SearchPlanSubAgent",
    instructions=SEARCH_PLAN_SUBAGENT_PROMPT,
    output_type=WebSearchPlan,
)

@function_tool
async def search_plan_tool(context: RunContextWrapper[CustomSession]) -> WebSearchPlan:
    """Generate a web search plan for the user's business idea using session context."""
    # Get the session from the context
    session = context.context

    # Run the web search plan sub-agent with session context
    search_plan = await Runner.run(search_plan_subagent, "Create or modify a web search plan based on the conversation context", session=session)
    return search_plan.final_output
    
    

search_plan_agent = Agent(
    name="SearchPlanAgent",
    instructions=SEARCH_PLAN_AGENT_PROMPT,
    model="gpt-4o",
    tools=[search_plan_tool],
)
