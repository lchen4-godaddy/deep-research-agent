from agents import function_tool

from src.tool_agents.research.query_writer_tool import query_writer_tool
from src.tools.web_search_tool import web_search

from src.agent_memory import AGENT_MEMORY


async def researcher(research_question: str) -> bool:
    """
    Conduct web research using the research plan and the research tools provided.
    
    Args:
        research_question: str - the research question to answer
        
    Returns:
        bool - True if the research was successful, False otherwise
    """
    try:
        queries = await query_writer_tool(research_question)
        results = []
        for query in queries:
            search_results = await web_search(query)
            results.extend(search_results)

        await AGENT_MEMORY.add_to_research_dump(research_question, results)

        return True
    except Exception as e:
        return False

@function_tool
async def researcher_tool(research_question: str) -> bool:
    """
    Function tool wrapper for researcher functionality.
    Conduct web research using the research plan and the research tools provided.
    
    Args:
        research_question: str - the research question to answer
        
    Returns:
        bool - True if the research was successful, False otherwise
    """
    return await researcher(research_question)