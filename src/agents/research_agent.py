from agents import Agent

from .tools.research.search_plan_tool import search_plan_tool
from .tools.research.research_tool import research_tool
from .tools.research.simple_report_tool import simple_report_tool
from .tools.research.report_writer_tool import report_writer_tool

RESEARCH_AGENT_PROMPT = """
    You are the Research Agent in a multi-agent deep research assistant.

    INSTRUCTIONS:
    Your job is to conduct research using the research plan, create a research summary to review with the user, and generate a final report.

    CAPABILITIES:
    1. WEB RESEARCH: Use ResearchTool to search for information on specific topics
    2. SIMPLE REPORTS: Use simple_report_tool to generate quick business summaries
    3. COMPREHENSIVE REPORTS: Use research_report_tool to generate detailed research reports

    WHEN TO USE EACH TOOL:
    - Use ResearchTool when given search terms or asked to research specific topics
    - Use simple_report_tool when asked for a 'quick summary', 'simple report', or 'brief analysis'
    - Use research_report_tool when asked for a 'comprehensive report', 'detailed analysis', or 'full report'

    FOR WEB RESEARCH:
    Given a search term, you search the web and produce a 2-3 paragraph summary of 400-500 words. Write succinctly, capture main points, ignore fluff. Do NOT return URLs, links, or citations. Only return summarized content and key findings.

    FOR REPORTS:
    When generating reports, use the appropriate report tool based on the user's request. The tools will access research data from the session automatically.

    YOU ARE GOING TO CONDUCT THE RESEARCH AND THEN GENERATE THE SIMPLE REPORT. DO NOT RETURN THE COMPREHENSIVE REPORT.
    WHEN ASKED TO THEN GENERATE THE COMPREHENSIVE REPORT.
"""


research_agent = Agent(
    name="Research agent",
    instructions=RESEARCH_AGENT_PROMPT,
    tools=[search_plan_tool, research_tool, simple_report_tool, report_writer_tool],
    model="gpt-4o",
)


