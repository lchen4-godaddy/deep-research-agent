from agents import Agent, Runner

async def contextual_summary_tool(research_question: str, raw_text: str) -> str:
    """Summarize a raw text chunk from a research source, contextualized to the research question.
    
    Args:
        research_question: str - the research question to contextualize the summary to
        raw_text: str - the raw text chunk to summarize
    """

    contextual_summarizer = Agent(
        name="Contextual Summary Tool-Agent",
        instructions=f"""
        You are a contextual summarizer, summarizing information from research sources.
        Given the following research question, summarize the raw text chunk (passed as input), contextualized to the research question.
        Make sure to include relevant statistics, data, and other information that is relevant to the research question.
        If certain statistics are cited by other sources, cite it with the url or the source name at the end of the sentence.
        Research question: {research_question}
        """,
        model="o4-mini",
    )
    
    summary = await Runner.run(contextual_summarizer, raw_text)

    return summary.final_output