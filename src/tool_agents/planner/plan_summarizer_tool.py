from agents import Agent, Runner, function_tool

from ...globals import CURRENT_SESSION

@function_tool
async def plan_summarizer_tool() -> str:
    """Summarize the research plan for the user to review."""
    
    # Get the research plan from the session
    research_plan = await CURRENT_SESSION.get_tool_output("plan_writer_tool")

    summarizer = Agent(
        name="PlanSummarizerToolAgent",
        instructions="""
        You are a research plan summarizer.
        Create a concise, clear summary of the research plan for the user to review.
        Leave the name and description as is.
        Keep headers and section titles the same, only summarize the sections of developed research questions and ideas.
        """,
        model="o4-mini",
    )
    
    summary = await Runner.run(summarizer, str(research_plan))
    await CURRENT_SESSION.store_tool_output("plan_summarizer_tool", summary.final_output)
    
    return summary.final_output