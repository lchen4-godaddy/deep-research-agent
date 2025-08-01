from agents import Agent, Runner, function_tool

from src.tools.researcher_tool import researcher_tool

from src.agent_memory import AGENT_MEMORY

RESEARCHER_PROMPT = """
    You are the Research Tool-Agent.
    Given a research plan, extract each research question and use the researcher_tool to conduct research.
    The researcher_tool will save the research results to the agent memory, and return whether the research was successful or not.
    Once you have have called the researcher_tool on every research question and received a result from each call, you should output "Done".
    """

@function_tool
async def research_finished() -> None:
    """Set the state research_finished to True."""
    AGENT_MEMORY.set_state("research_finished", True)

@function_tool
async def research_tool() -> str:
    """Conduct web research using the research plan and the research tools provided."""
    
    researcher = Agent(
        name="Research Tool-Agent",
        instructions=RESEARCHER_PROMPT,
        tools=[researcher_tool],
        model="o4-mini",
    )
    
    research_plan = await AGENT_MEMORY.get_research_plan()

    result = await Runner.run(researcher, research_plan)

    print(result.final_output)

    return True