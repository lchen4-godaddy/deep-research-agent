from agents import Agent, Runner, function_tool

from ....globals import CURRENT_SESSION as session

PLAN_WRITER_PROMPT = """
    You are the Plan Writer, a tool-agent for the Planner Agent.

    INSTRUCTIONS:
    Use the conversation context to create a COMPREHENSIVE research plan.
    DO NOT make up information for any of the user-provided information.
    Use ONLY the information provided in the conversation context.
    Filter out any extraneous or irrelevant information from the conversation context that is not pertinent to creating a research plan.
    If anything under the information section is missing, note it as "To be determined" rather than making it up.
    If the user doesn't indicate any preference or requirements for research areas, use the structure-provided research areas below and develop research questions for each area.

    Plan Structure:
    - Information:
        - Product Name: [Use the actual product name from conversation]
        - Description: [Generate a concise, refined description of the product using the user's description from the conversation, < 200 words]
        - Features and Scope
    - Research Areas:
        - Market Analysis:
            - Industry Trends / Product Validation
            - Target Audience
            - Competitors
        - Business Model / Financial Research:
            - Pricing
            - Revenue Streams
        - Marketing Research:
            - Marketing Channels
            - Marketing Strategies
        - Technical and Legal Research:
            - Technical Feasibility
            - Legal Requirements
            - IP Protection
            - Regulatory Compliance
    """

@function_tool
async def plan_writer_tool() -> str:
    """Create a research plan for the user's business idea using session conversation history."""

    # Get the conversation history from the session
    conversation_history = await session.get_items()

    plan_writer = Agent(
    name="PlanWriterToolAgent",
    instructions=PLAN_WRITER_PROMPT,
    model="o4-mini",
    )
    
    # Run the plan_writer agent
    research_plan = await Runner.run(plan_writer, conversation_history)
    
    return research_plan.final_output