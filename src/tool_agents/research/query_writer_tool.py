from agents import Agent, Runner
from typing import List

async def query_writer_tool(research_question: str) -> List[str]:
    """Given a research question, generate a list of search queries to use for web search.
    
    Args:
        research_question: str - the research question to generate search queries for
    """
    
    # Number of search queries is hardcoded to 3, later we can make it dynamic
    search_query_generator = Agent(
        name="Search Query Generator Tool-Agent",
        instructions="""
            You are a search term generator.
            Given a research question, generate 3 search queries to use for web search.
            The search queries should be short phrases with important keywords, and should target the research question.
            Separate each search query with a comma, without any new lines.
            """,
        model="gpt-4.1",
    )
    
    search_queries = await Runner.run(search_query_generator, research_question)
    queries_list = search_queries.final_output.split(",")

    return queries_list