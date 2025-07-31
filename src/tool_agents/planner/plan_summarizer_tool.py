from agents import Agent, Runner, function_tool

from src.agent_memory import AGENT_MEMORY

@function_tool
async def plan_summarizer_tool() -> str:
    """Summarize the research plan for the user to review."""
    
    # Get the research plan from the session
    research_plan = await AGENT_MEMORY.get_tool_output("plan_writer_tool")

    plan_summarizer = Agent(
        name="Plan Summarizer Tool-Agent",
        instructions="""
            You are a research plan summarizer.
            Create a concise, clear summary of the research plan for the user to review.
            Leave the name and description as is.
            Keep headers and section titles the same, only summarize the sections of developed research questions and ideas.
            """,
        model="o4-mini",
    )
    
    summary = await Runner.run(plan_summarizer, str(research_plan))
    await AGENT_MEMORY.store_tool_output("plan_summarizer_tool", summary.final_output)
    
    return summary.final_output