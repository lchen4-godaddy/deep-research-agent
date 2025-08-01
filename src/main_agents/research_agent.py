from agents import Agent, function_tool

from src.tool_agents.research.research_tool import research_tool
from src.tool_agents.research.report_writer_tool import report_writer_tool

from src.agent_memory import AGENT_MEMORY

RESEARCH_AGENT_PROMPT = """
    You are the Research Agent in a multi-agent deep research assistant.

    Instructions:
    Your job is to facilitate the research process.
    First, clear the session using the clear_session tool. You don't need the previous conversation context.
    You will call the research_tool to conduct research, and wait for the research to finish.
    Once the research is finished (research_tool will return True), call the report_writer_tool to generate a report.
    Respond to the user in the following format:
    ```
    Here's the research report, let me know if you have any questions!
    [output from report_writer_tool]
    ```
    
    Tools:
    - research_tool: Conduct research using the research plan.
    - report_writer_tool: Generate a report from the research results.
"""

@function_tool
async def clear_session() -> None:
    """Clear the session."""
    await AGENT_MEMORY.clear_session()

research_agent = Agent(
    name="Research Agent",
    instructions=RESEARCH_AGENT_PROMPT,
    tools=[research_tool, report_writer_tool],
    model="o4-mini",
)