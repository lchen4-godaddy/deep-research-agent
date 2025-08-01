from agents import Agent, Runner, function_tool

from src.tools.researcher_tool import researcher_tool

from src.agent_memory import AGENT_MEMORY

RESEARCHER_PROMPT = """
    You are the Research Tool-Agent.
    Given a research plan, extract each research question and use the researcher_tool to conduct research.
    
    1. Extract the research questions from the research plan.
    2. Call the researcher_tool once for each research question.
    
    """

@function_tool
async def research_tool() -> bool:
    """Conduct web research using the research plan and the research tools provided."""
    
    researcher = Agent(
        name="Research Tool-Agent",
        instructions=RESEARCHER_PROMPT,
        tools=[researcher_tool],
        model="gpt-4.1",
    )
    
    research_plan = await AGENT_MEMORY.get_research_plan()
    
    if not research_plan or len(research_plan.strip()) < 50:
        return "Error: No valid research plan found. Cannot proceed with research."
    
    print(f"🔍 Research Tool: Starting research with plan length: {len(research_plan)}")
    print(f"🔍 Research Tool: Plan preview: {research_plan[:200]}...")

    result = await Runner.run(researcher, research_plan)

    print(f"🔍 Research Tool: Research completed with output: {result.final_output}")
    
    # Validate that research was actually performed
    research_dump = await AGENT_MEMORY.get_research_dump()
    print(f"🔍 Research Tool: Research dump has {len(research_dump)} entries")
    
    # Check if meaningful research was conducted
    if len(research_dump) == 0:
        return "Error: No research data was collected. Research failed."
    
    # Check if we have research for multiple questions
    question_count = len(research_dump.keys())
    if question_count < 2:
        return f"Error: Only {question_count} research questions were processed. Expected at least 2. Research incomplete."
    
    # Check if each question has meaningful results
    for question, results in research_dump.items():
        if not results or len(results) == 0:
            return f"Error: No results found for question: {question}. Research incomplete."
    
    print(f"🔍 Research Tool: Successfully researched {question_count} questions with {sum(len(results) for results in research_dump.values())} total results")
    return True