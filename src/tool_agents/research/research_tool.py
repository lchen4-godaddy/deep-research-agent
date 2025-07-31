from agents import Agent, Runner, function_tool

from src.tools.researcher_tool import researcher_tool

from src.agent_memory import AGENT_MEMORY

RESEARCH_PROMPT = """
    You are the Research Tool-Agent.
    Given a research plan, extract each research question and use the researcher_tool to conduct research.
    The researcher_tool will save the research results to the agent memory, and return whether the research was successful or not.
    """

@function_tool
async def research_tool() -> str:
    """Conduct web research using the research plan and the research tools provided."""
    
    researcher = Agent(
        name="Research Tool-Agent",
        instructions=RESEARCH_PROMPT,
        tools=[researcher_tool],
        model="o4-mini",
    )
    
    research_plan = await AGENT_MEMORY.get_tool_output("plan_writer_tool")

    result = await Runner.run(researcher, research_plan)

    return result.final_output