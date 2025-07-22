from agents import Agent, Runner, function_tool

from ....globals import CURRENT_SESSION as session

SIMPLE_REPORT_PROMPT = """
    You are a business analyst creating a quick executive summary. You will receive research 
    findings and need to create a concise business-focused summary.

    SimpleReportData structure:
    - executive_summary: Brief executive summary (50-100 words)
    - key_findings: 3-5 most important findings
    - recommendations: 3-5 actionable recommendations
    - next_steps: 2-3 immediate next steps
    - full_summary: Complete simple report text

    REQUIREMENTS:
    - Keep the summary brief (300-500 words total)
    - Focus on the most critical insights only
    - Provide actionable recommendations
    - Use clear, professional language
    - Be direct and to the point

    OUTPUT FORMAT:
    1. Executive Summary (2-3 sentences)
    2. Key Findings (3-5 bullet points)
    3. Recommendations (3-5 action items)
    4. Next Steps (2-3 immediate actions)

    Do not include URLs, citations, or lengthy explanations. Focus on actionable insights.
    """

@function_tool
async def simple_report_tool() -> str:
    """Generate a simple business report from research results using session context."""
    
    simple_report_subagent = Agent(
        name="SimpleReportSubAgent",
        instructions=SIMPLE_REPORT_PROMPT,
        model="gpt-4o-mini",
    )

    # Get research results from session if available
    research_data = await session.get_tool_output("research_tool")

    # Run the research report sub-agent
    result = await Runner.run(simple_report_subagent, research_data)
    return result.final_output
