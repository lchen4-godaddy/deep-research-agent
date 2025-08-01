from ast import Str
from agents import Agent, Runner, function_tool
from typing import List, Tuple

from src.agent_memory import AGENT_MEMORY

REPORT_WRITER_PROMPT = """
    You are the Report Writer, in charge of generating a comprehensive research report given a research plan and a set of research insights.

    CRITICAL REQUIREMENTS:
    - You MUST generate a comprehensive research report
    - You MUST use the research plan as the framework
    - You MUST incorporate research insights from the research dump
    - You CANNOT provide a generic or empty report
    - The report MUST be detailed and actionable

    OBJECTIVE:
    Generate a comprehensive research report from research results using the research plan and research dump content.

    MANDATORY PROCESS:
    1. Review the research plan - the report needs to comprehensively cover all research areas
    2. Get all of the research insights from the research dump using the get_research_dump tool
    3. Build the research report using a professional tone and style
    4. Use the research insights to cite sources and provide evidence
    5. Ensure the report is actionable and helps the user actualize their idea

    OUTPUT FORMAT (produce in markdown format):

    1. **Information** [from the research plan]

    2. **Introduction**
        - Overview of research topics covered in the report.

    3. **Research Areas**
        - Market Analysis
        - Business Model & Financial Research
        - Marketing Research
        - Technical & Legal Research
    
    4. **Conclusion**
        - Summarize the research findings.
        - Validate the user's idea based on the research findings.
        - Suggest next steps for the user to take.

    5. **References**
        - Number all of the references used in the report. This will also allow for simple citation.
        - List all of the sources, with the source title and the URL.
        - Template: 1. [Source Title]: [URL]
    """

@function_tool
async def get_research_dump() -> str:
    """Get the research dump."""
    research_dump = await AGENT_MEMORY.get_research_dump()
    return str(research_dump)
    
@function_tool
async def report_writer_tool() -> str:
    """Generate a comprehensive research report from research results using the research plan and research dump content."""    
    
    research_plan = await AGENT_MEMORY.get_research_plan()
    
    report_writer = Agent(
        name="Report Writer Tool-Agent", 
        instructions=REPORT_WRITER_PROMPT,
        model="gpt-4.1",
        tools=[get_research_dump],
    )
        
    # Run the research report sub-agent
    result = await Runner.run(report_writer, research_plan)
    report_content = result.final_output

    # Store the report in the agent memory
    await AGENT_MEMORY.store_report(report_content)

    # Set the state report_generated to True
    AGENT_MEMORY.set_state("report_generated", True)

    return report_content