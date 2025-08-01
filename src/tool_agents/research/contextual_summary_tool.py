from agents import Agent, Runner

async def contextual_summary_tool(research_question: str, raw_text: str) -> str:
    """Summarize a raw text chunk from a research source, contextualized to the research question.
    
    Args:
        research_question: str - the research question to contextualize the summary to
        raw_text: str - the raw text chunk to summarize
    """
    
    # Truncate content if it's too long to avoid context window issues
    # Most LLMs have context limits around 8k-32k tokens, so we'll be conservative
    # Assuming roughly 4 characters per token, we'll limit to ~6000 tokens = ~24k characters
    MAX_CONTENT_LENGTH = 24000
    
    if len(raw_text) > MAX_CONTENT_LENGTH:
        # Truncate to the first MAX_CONTENT_LENGTH characters
        # Try to break at a sentence boundary if possible
        truncated_text = raw_text[:MAX_CONTENT_LENGTH]
        
        # Try to find the last complete sentence
        last_period = truncated_text.rfind('.')
        last_exclamation = truncated_text.rfind('!')
        last_question = truncated_text.rfind('?')
        
        # Find the latest sentence ending
        sentence_end = max(last_period, last_exclamation, last_question)
        
        if sentence_end > MAX_CONTENT_LENGTH * 0.8:  # Only use sentence boundary if it's not too early
            truncated_text = truncated_text[:sentence_end + 1]
        
        raw_text = truncated_text + "\n\n[Content truncated due to length constraints]"

    contextual_summarizer = Agent(
        name="Contextual Summary Tool-Agent",
        instructions=f"""
        You are a contextual summarizer, summarizing information from research sources.
        Given the following research question, summarize the raw text chunk (passed as input), contextualized to the research question.
        Make sure to include relevant statistics, data, and other information that is relevant to the research question.
        If certain statistics are cited by other sources, cite it with the url or the source name at the end of the sentence.
        The summary should be concise and to the point, and should be no more than 200 words long.
        Research question: {research_question}
        """,
        model="gpt-4.1",
    )
    
    try:
        summary = await Runner.run(contextual_summarizer, raw_text)
        return summary.final_output
    except Exception as e:
        # If summarization fails due to context window or other issues, return a fallback
        if "context_length_exceeded" in str(e) or "context window" in str(e).lower():
            return f"Content too large to summarize. Key points from the source: {raw_text[:500]}..."
        else:
            return f"Error summarizing content: {str(e)}"