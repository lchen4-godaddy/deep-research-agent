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
        print(f"🔍 Researcher: Starting research for question: {research_question}")
        
        queries = await query_writer_tool(research_question)
        print(f"🔍 Researcher: Generated {len(queries)} queries")
        
        results = []
        for i, query in enumerate(queries):
            print(f"🔍 Researcher: Searching query {i+1}: {query}")
            search_results = await web_search(query)
            print(f"🔍 Researcher: Got {len(search_results)} results for query {i+1}")
            results.extend(search_results)

        print(f"🔍 Researcher: Total results collected: {len(results)}")
        await AGENT_MEMORY.add_to_research_dump(research_question, results)
        print(f"🔍 Researcher: Added results to research dump for question: {research_question}")

        return True
    except Exception as e:
        print(f"❌ Researcher: Error during research: {e}")
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