from pydantic import BaseModel

from agents import Agent, WebSearchTool
from agents.model_settings import ModelSettings

PROMPT = """
    You are the Research Agent in a multi-agent research assistant system.
    Your job is to evaluate each user input and the current system stage, and determine a task and the appropriate agent (research_planner, research, response) to handoff the task to.

"""


research_agent = Agent(
    name="ResearchAgent",
    instructions=PROMPT,
    model="gpt-4.1",
    tools=[WebSearchTool()],
    model_settings=ModelSettings(tool_choice="required"),
)