from agents import Agent, WebSearchTool, Runner, function_tool
from ....globals import CURRENT_SESSION as session

RESEARCH_PROMPT = """
    You are a research assistant.
    Given a Search Plan, you use the WebSearchTool and produce a research dump with adetailed summary of the results.

    Research Dump structure:
    - topic: The research topic or question
    - search_query: The search query used
    - summary: The research summary

    Instructions:
    - Each summary from each search query should be detailed, highlighting insights and key findings with context.
    - The research dump will be used by the simple_report_tool to generate a summary, so it is vital you capture the essence and ignore any fluff.
    - IMPORTANT: Do NOT return URLs, links, or citations. Only return the summarized content and key findings from the web search results.
    - Make sure the search is quick and focused.
    - Output to the user when you are starting the research and periodically update them on your progress.

    Example:
    FOR WEB RESEARCH:
    Given a search term, you search the web and produce a 2-3 paragraph summary of 400-500 words.
    Write succinctly, capture main points, ignore fluff.
    Do NOT return URLs, links, or citations.
    Only return summarized content and key findings.
    """

@function_tool
async def research_tool() -> str:
    """Conduct web research using the research subagent."""
    
    research_subagent = Agent(
        name="ResearchSubAgent", 
        instructions=RESEARCH_PROMPT,
        tools=[WebSearchTool()],
        model="gpt-4o-mini",
    )
    
    items = await session.get_tool_output("search_plan_tool")

    result = await Runner.run(research_subagent, items)

    return result.final_output