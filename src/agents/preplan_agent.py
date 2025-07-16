from pydantic import BaseModel

from agents import Agent, Runner, function_tool, RunContextWrapper
from ..custom_session import CustomSession

PREPLAN_AGENT_PROMPT = """
    You are the Pre-Plan Agent in a multi-agent deep research assistant.
    Your job is to gather detailed information about the user's business or product idea, business context, and specific research interests.

    Guidelines:
    - Ask the user for all relevant details about their idea, including product/service name, industry, goals, target audience, and any known competitors.
    - Identify and record the user's main research questions or areas of interest.
    - Use the prewrite_tool to create a structured pre-write summary when you have enough information.
    - Offer suggestions for additional context that may improve the quality of the research.
    - Confirm with the user that all necessary context and research areas have been captured before proceeding.

    IMPORTANT: When you have gathered sufficient information about the user's business idea, you MUST use the prewrite_tool to create a structured pre-write summary. Do not manually create the summary - use the tool.
    IMPORTANT RULES:
    1. Only use the prewrite_tool once you have gotten permission from the user to proceed with a pre-write or modify the existing one.
    2. If the user asks to "see" or "get" the pre-write, retrieve it from the session data - DO NOT call the tool again.
      a. You may only format the pre-write in a way that is easy to read and understand. Do not summarize or add any additional information.
    Your objective is to ensure all essential background information is gathered and validated by the user before moving to search planning.

"""

PREWRITER_PROMPT = """
    You are the Pre-Writer Sub-Agent.
    Given the session context, create or modify an existing pre-write for the user's business or product idea.

    PreWrite structure:
    - idea: str (keep it concise)
    - context: list[ContextItem] (e.g. location: San Francisco, industry: cosmetics, etc.)
    - user_requested_research_areas: list[str] (e.g. market research, business model, etc.)

    ContextItem structure:
    - type: str (e.g. location, industry, etc.)
    - description: str (e.g. San Francisco, cosmetics, etc.)

    IMPORTANT: If a pre-write already exists and modifications are requested, use the current pre-write as a template and modify the existing pre-write. Only modify the contents that the user requests. Do not create a new pre-write from scratch, and do not modify fields which are not explicitly requested.

"""

class ContextItem(BaseModel):
    type: str
    """The type of context (e.g. location, industry, etc.)"""
    description: str
    """The description of the context (e.g. San Francisco, cosmetics, etc.)"""

class PreWrite(BaseModel):
    idea: str
    """The main business or product idea"""
    context: list[ContextItem]
    """User-provided context for the purpose of the research, business context, etc."""
    user_requested_research_areas: list[str]
    """List of research areas requested by user"""

prewriter_subagent = Agent(
    name="PreWriterSubAgent",
    instructions=PREWRITER_PROMPT,
    output_type=PreWrite,
)

@function_tool
async def prewrite_tool(context: RunContextWrapper[CustomSession]) -> PreWrite:
    """Create a pre-write for the user's business idea using session context."""
    # Get the session from the context
    session = context.context
    
    # Run the prewriter agent with session context
    # The session contains all the conversation history needed
    prewrite = await Runner.run(prewriter_subagent, "Create or modify a pre-write based on the conversation context", session=session)
    return prewrite.final_output


preplan_agent = Agent(
    name="PrePlanAgent",
    instructions=PREPLAN_AGENT_PROMPT,
    tools=[prewrite_tool],
    model="gpt-4o",
)