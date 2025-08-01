from agents import Agent, Runner, function_tool

from src.agent_memory import AGENT_MEMORY

@function_tool
async def plan_summarizer_tool() -> str:
    """Summarize the research plan for the user to review."""
    
    # Get the research plan from the session
    research_plan = await AGENT_MEMORY.get_research_plan()

    plan_summarizer = Agent(
        name="Plan Summarizer Tool-Agent",
        instructions="""
            You are a research plan summarizer.
            Create a concise, clear summary of the research plan for the user to review.
            Leave the name and description as is.
            Keep headers and section titles the same, only summarize the sections of developed research questions and ideas.
            """,
        model="gpt-4.1",
    )
    
    summary = await Runner.run(plan_summarizer, str(research_plan))
    
    return summary.final_output