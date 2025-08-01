from agents import Agent, Runner, function_tool
from typing import List, Tuple

from src.agent_memory import AGENT_MEMORY

REPORT_WRITER_PROMPT = """
    You are the Report Writer, in charge of generating a comprehensive research report given a research plan and a set of research insights.

    OBJECTIVE:
    Generate a comprehensive research report from research results using the research plan and research dump content.

    PROCESS:
    1. Review the research plan - the report needs to comprehensively cover all research areas and should be framed to help the user actualize their idea.
    2. Use the get_from_research_dump_by_question(research_question) tool to get the research insights from each research conducted on the research questions.
        - Research insights are a list of tuples, each containing ((Title, URL), summary) where Title is the page title and URL is the source URL.
    3. Build the research report. Use a professional tone and style, and use the research insights to cite sources.

    OUTPUT FORMAT (produce in markdown format):

    1. **Information** [from the research plan]

    2. **Introduction**
        - Overview of research topics covered in the report.

    3. **Research Areas**
        - Market Analysis
        - Business Model & Financial Research
        - Marketing Research
        - Technical & Legal Research
    
    3. **Conclusion**
        - Summarize the research findings.
        - Validate the user's idea based on the research findings.
        - Suggest next steps for the user to take.

    4. **References**
        - Number all of the references used in the report. This will also allow for simple citation.
        - List all of the sources, with the source title and the URL.
        - Template: 1. [Source Title]: [URL]
    """

@function_tool
async def get_from_research_dump_by_question(research_question: str) -> List[Tuple[Tuple[str, str], str]]:
    """Get the research results for a specific question from the research dump."""
    return await AGENT_MEMORY.get_from_research_dump_by_question(research_question)
    
@function_tool
async def report_writer_tool() -> str:
    """Generate a comprehensive research report from research results using the research plan and research dump content."""    
    
    research_plan = await AGENT_MEMORY.get_research_plan()

    report_writer = Agent(
        name="Report Writer Tool-Agent", 
        instructions=REPORT_WRITER_PROMPT,
        model="o4-mini",
        tools=[get_from_research_dump_by_question],
    )
        
    # Run the research report sub-agent
    result = await Runner.run(report_writer, research_plan)

    # Set the state report_generated to True
    await AGENT_MEMORY.set_state("report_generated", True)

    return result.final_output