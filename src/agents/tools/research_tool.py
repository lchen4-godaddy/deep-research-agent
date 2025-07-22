from agents import Agent, WebSearchTool, Runner, function_tool
from ...globals import CURRENT_SESSION as session

RESEARCH_PROMPT = """
    You are a research assistant.
    Given a search term, you search the web for that term and produce a long summary of the results.

    ResearchResult structure:
    - topic: The research topic or question
    - search_query: The search query used
    - summary: The research summary

    Instructions:
    - The summary must be 2-3 paragraphs (400-500 words).
    - Capture the main points.
    - Write succinctly; no need for complete sentences or perfect grammar.
    - This will be consumed by someone synthesizing a report, so it is vital you capture the essence and ignore any fluff.
    - Do not include any additional commentary other than the summary itself.
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