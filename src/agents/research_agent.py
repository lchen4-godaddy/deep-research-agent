import json
import asyncio
from typing import Dict, List, Any
from pydantic import BaseModel

from agents import Agent, WebSearchTool, Runner, function_tool, RunContextWrapper
from agents.model_settings import ModelSettings
from ..custom_session import CustomSession

INSTRUCTIONS = (
    "You are a research assistant with multiple capabilities. You can conduct web research and generate reports.\n\n"
    
    "CAPABILITIES:\n"
    "1. WEB RESEARCH: Use ResearchTool to search for information on specific topics\n"
    "2. SIMPLE REPORTS: Use simple_report_tool to generate quick business summaries\n"
    "3. COMPREHENSIVE REPORTS: Use research_report_tool to generate detailed research reports\n\n"
    
    "WHEN TO USE EACH TOOL:\n"
    "- Use ResearchTool when given search terms or asked to research specific topics\n"
    "- Use simple_report_tool when asked for a 'quick summary', 'simple report', or 'brief analysis'\n"
    "- Use research_report_tool when asked for a 'comprehensive report', 'detailed analysis', or 'full report'\n\n"
    
    "FOR WEB RESEARCH:\n"
    "Given a search term, you search the web and produce a 2-3 paragraph summary of 400-500 words. "
    "Write succinctly, capture main points, ignore fluff. Do NOT return URLs, links, or citations. "
    "Only return summarized content and key findings.\n\n"
    
    "FOR REPORTS:\n"
    "When generating reports, use the appropriate report tool based on the user's request. "
    "The tools will access research data from the session automatically."



    """YOU ARE GOING TO CONDUCT THE RESEARCH AND THEN GENERATE THE SIMPLE REPORT. DO NOT RETURN THE COMPREHENSIVE REPORT.
    WHEN ASKED TO THEN GENERATE THE COMPREHENSIVE REPORT."""
)


class ResearchResult(BaseModel):
    topic: str
    """The research topic or question"""
    
    search_query: str
    """The search query used"""
    
    summary: str
    """The research summary"""

class ResearchPlanResults(BaseModel):
    topic: str
    """The main research topic"""
    
    business_context: Dict[str, Any]
    """Business context from the research plan"""
    
    research_results: List[ResearchResult]
    """List of research results for each topic"""
    
    completion_status: str
    """Status of the research completion"""

# Import the report data models
class SimpleReportData(BaseModel):
    executive_summary: str
    """Brief executive summary (50-100 words)"""
    
    key_findings: List[str]
    """3-5 most important findings"""
    
    recommendations: List[str]
    """3-5 actionable recommendations"""
    
    next_steps: List[str]
    """2-3 immediate next steps"""
    
    full_summary: str
    """Complete simple report text"""

class ResearchReportData(BaseModel):
    executive_summary: str
    """A comprehensive executive summary (200-300 words)"""
    
    full_report: str
    """The complete research report in markdown format"""
    
    key_insights: List[str]
    """List of 6-10 most important insights"""
    
    recommendations: List[str]
    """List of 6-10 specific actionable recommendations"""
    
    follow_up_research: List[str]
    """5-7 areas needing additional research"""
    
    research_gaps: List[str]
    """3-5 areas where research was insufficient"""

# Sub-agents for report generation
SIMPLE_REPORT_PROMPT = (
    "You are a business analyst creating a quick executive summary. You will receive research "
    "findings and need to create a concise business-focused summary.\n\n"
    
    "REQUIREMENTS:\n"
    "- Keep the summary brief (300-500 words total)\n"
    "- Focus on the most critical insights only\n"
    "- Provide actionable recommendations\n"
    "- Use clear, professional language\n"
    "- Be direct and to the point\n\n"
    
    "OUTPUT FORMAT:\n"
    "1. Executive Summary (2-3 sentences)\n"
    "2. Key Findings (3-5 bullet points)\n"
    "3. Recommendations (3-5 action items)\n"
    "4. Next Steps (2-3 immediate actions)\n\n"
    
    "Do not include URLs, citations, or lengthy explanations. Focus on actionable insights."
)

RESEARCH_REPORT_PROMPT = (
    "You are a business analyst creating a comprehensive research report. You will receive research "
    "results from multiple topics and need to synthesize them into a structured, professional report.\n\n"
    
    "REPORT STRUCTURE:\n"
    "1. Executive Summary (2-3 paragraphs)\n"
    "2. Key Findings (organized by topic)\n"
    "3. Market Analysis (synthesis of market data)\n"
    "4. Opportunities & Challenges\n"
    "5. Strategic Recommendations\n"
    "6. Implementation Roadmap\n"
    "7. Risk Assessment\n"
    "8. Conclusion\n\n"
    
    "REQUIREMENTS:\n"
    "- Keep the report comprehensive but focused (1000-1500 words)\n"
    "- Use professional business language\n"
    "- Include markdown formatting with headers and bullet points\n"
    "- Synthesize findings across all research areas\n"
    "- Provide specific, actionable recommendations\n"
    "- Highlight key statistics and trends\n"
    "- Connect insights to business objectives\n\n"
    
    "Do not include URLs or citations. Focus on synthesized insights and strategic analysis."

    """
        Example:
        # Research Report: Starting a Taco Truck

        ## Executive Summary

        Launching a taco truck in an urban area represents a lucrative opportunity given the growing demand for mobile dining options. The food truck industry experienced substantial growth, with revenues projected to reach $1.5 billion in 2023 and expected to maintain a compound annual growth rate (CAGR) of 6.8% through 2030. To successfully establish a taco truck, it’s essential to understand both the competitive landscape and local consumer preferences. Engaging marketing strategies, a diverse menu, and compliance with health and zoning regulations are critical components for building a successful brand in this thriving sector.

        ## Key Insights

        1. Projected food truck market growth of $1.5 billion in 2023
        2. Average daily revenues for taco trucks range from $500 to $2,000
        3. Important demographic of customers aged 25 to 44, particularly during lunch hours
        4. Navigating local permits and health regulations is crucial for operation
        5. The food truck industry is increasingly leveraging social media for marketing

        ## Recommendations

        1. Identify prime locations for operations based on foot traffic analysis and community events.
        2. Diversify the menu to include not just tacos but also sides and beverages to boost order value.
        3. Engage with local events and festivals for community visibility and potential sales boosts.
        4. Utilize data-driven insights to establish optimal pricing strategies catering to the target demographic.
        5. Implement a robust social media strategy for real-time marketing and customer engagement.

        ## Full Report

        ### Executive Summary
        Launching a taco truck in an urban area presents a significant opportunity, given the increasing demand for convenient dining options. The food truck industry has seen substantial growth, with projected revenues reaching approximately $1.5 billion in 2023. This trend is primarily driven by urbanization and changing consumer lifestyles that favor mobile food services. However, the competitive landscape in cities like Los Angeles and New York is intense, necessitating a clear understanding of market dynamics and customer preferences.

        To ensure profitability, understanding regional regulations, startup costs, and effective marketing strategies is crucial. Emphasizing diverse menu offerings, especially variations of popular tacos catered to local tastes, can help differentiate the business. Furthermore, leveraging social media and community engagement is vital for driving awareness and building a loyal customer base.

        ### Key Findings
        - **Market Demand**: The food truck market is anticipated to grow at a CAGR of 6.8%, driven by consumer demand for convenient dining.
        - **Competition**: Major urban areas have dense food truck markets, necessitating a clear differentiation strategy.
        - **Startup Costs**: Initial expenses can range from $40,000 to $150,000 for the truck and additional $10,000 to $30,000 for kitchen equipment.
        - **Permitting**: Navigating local regulations and obtaining necessary permits are critical for compliance. Costs vary, with permits ranging from $50 to over $3,000.
        - **Revenue Potential**: Daily revenues can range from $500 to $2,000, translating to annual revenues between $250,000 and $500,000.
        - **Demographics**: The primary customer base consists of individuals aged 25 to 44, with 47% in the 18 to 34 age bracket, indicating a focus on younger, urban professionals.
        - **Menu Trends**: Offering traditional and innovative taco varieties can attract a wider customer base.
        - **Seasonality**: Summer typically sees higher sales due to outdoor events and increased pedestrian traffic.

        ### Recommendations
        1. **Strategic Location Selection**: Position the taco truck in high-foot traffic areas during peak hours (11 AM–2 PM) to maximize visibility and sales. 
        2. **Diverse Menu Development**: Incorporate various taco varieties and fusion options to appeal to diverse customer preferences. Consider seasonal specials to leverage fluctuations in demand.
        3. **Marketing Strategies**: Utilize social media platforms for real-time updates, promotions, and engaging visual content to attract younger demographics. Host launch events or collaborate with local businesses to raise awareness.
        4. **Compliance and Permits**: Prioritize obtaining all necessary permits and understanding local health and zoning regulations to avoid potential legal pitfalls.
        5. **Leverage Technology**: Integrate with food delivery platforms and mobile apps to enhance customer engagement and streamline operations.
        6. **Explore Additional Revenue Streams**: Consider catering services, event partnerships, and branded merchandise to diversify income.
        7. **Customer Engagement**: Offer promotions, such as discounts or free samples at launch, to encourage initial visits and build a loyal customer base.

        ### Market Analysis
        The taco truck sector is not just a food service; it’s part of a rapidly growing street food culture. Major urban areas have established vibrant food scenes, giving taco trucks an opportunity to thrive. The increasing preference for convenient, on-the-go dining further supports this market growth. Ensuring a competitive edge through innovative menu offerings and effective branding will be vital.

        ### Next Steps
        - **Conduct a Feasibility Study**: Analyze specific locations to determine traffic patterns and demographic profiles.
        - **Finalize Menu and Pricing**: Test menu items and determine optimal pricing strategies based on local market research.
        - **Develop a Marketing Plan**: Outline detailed marketing efforts, focusing on social media engagement and partnerships.
        - **Acquire Funding**: Explore funding options for purchasing and outfitting the taco truck, including potential loans or investor partnerships.
        - **Engage with Local Authorities**: Start the permitting process and establish relationships with local health departments and business associations.
        ## Research Gaps

        1. Understanding of long-term customer retention strategies in the food truck industry.
        2. Analysis of the impact of economic fluctuations on consumer spending in mobile food services.
        3. Trends affecting food delivery service integration within the taco truck business model.

        ## Follow-up Research Suggestions

        1. Conduct a detailed competitive analysis of existing taco trucks in the target area.
        2. Assess preferences for specific taco varieties to tailor the menu accordingly.
        3. Investigate local regulations further for any unique considerations or emerging trends specific to the city.

    """
)

RESEARCH_PROMPT = (
    "You are a research assistant. Given a search term, you search the web for that term and "
    "Output to the user when you are starting the research and periodically update them on your progress."
    "produce a long summary of the results. The summary must be 2-3 paragraphs"
    "words. Capture the main points. Write succinctly, no need to have complete sentences or good "
    "grammar. This will be consumed by someone synthesizing a report, so its vital you capture the "
    "essence and ignore any fluff. Do not include any additional commentary other than the summary "
    "itself. IMPORTANT: Do NOT return URLs, links, or citations. Only return the summarized content "
    "and key findings from the web search results. Make sure the search is quick and focused."
)

simple_report_subagent = Agent(
    name="SimpleReportSubAgent",
    instructions=SIMPLE_REPORT_PROMPT,
    model="gpt-4o-mini",
    output_type=SimpleReportData,
)

research_report_subagent = Agent(
    name="ResearchReportSubAgent", 
    instructions=RESEARCH_REPORT_PROMPT,
    model="gpt-4o-mini",
    output_type=ResearchReportData,
)

research_subagent = Agent(
    name="ResearchSubAgent", 
    instructions=RESEARCH_PROMPT,
    tools=[WebSearchTool()],
    model="gpt-4o-mini",
)

@function_tool
async def research_tool(context: RunContextWrapper[CustomSession]) -> str:
    """Conduct web research using the research subagent."""
    session = context.context
    
    # The research agent should pass the specific search term in the message
    # For now, we'll extract it from the conversation context or use a default
    
    # Get recent conversation to understand what to research
    research_topic = "business research"  # default
    
    if session:
        items = await session.get_items()
        # Look for the most recent user input to determine research topic
        if items:
            for item in reversed(items):
                if hasattr(item, 'content') and item.content:
                    research_topic = str(item.content)[:200]  # Use recent context
                    break
    
    research_request = f"Search term: {research_topic}\nReason for searching: Conducting research for user analysis"
    
    result = await Runner.run(research_subagent, research_request)
    research_result = str(result.final_output) if result.final_output else "No research results found"
    
    # Store the research result in session if available
    if session and hasattr(session, 'store_tool_output'):
        await session.store_tool_output("latest_research", {
            "topic": research_topic,
            "summary": research_result
        })
    
    return research_result


@function_tool
async def simple_report_tool(context: RunContextWrapper[CustomSession]) -> SimpleReportData:
    """Generate a simple business report from research results using session context."""
    session = context.context
    
    # Get research results from session if available
    research_data = None
    if session and hasattr(session, 'get_tool_output'):
        research_data = await session.get_tool_output("research_results")
        
        # If no research_results, try latest_research
        if not research_data:
            latest_research = await session.get_tool_output("latest_research")
            if latest_research:
                # Convert to expected format
                research_data = {
                    "topic": latest_research.get("topic", "Research Topic"),
                    "research_results": [{
                        "topic": latest_research.get("topic", "Research Topic"),
                        "summary": latest_research.get("summary", "No summary available")
                    }]
                }
    
    # If still no research data, conduct research first
    if not research_data:
        # Get the research topic from recent conversation
        research_topic = "business analysis"
        if session:
            items = await session.get_items()
            if items:
                for item in reversed(items):
                    if hasattr(item, 'content') and item.content:
                        research_topic = str(item.content)[:200]
                        break
        
        # Conduct research first
        print("🔍 No research data found. Conducting research first...")
        research_request = f"Search term: {research_topic}\nReason for searching: Research for simple report generation"
        result = await Runner.run(research_subagent, research_request)
        research_summary = str(result.final_output) if result.final_output else "No research results found"
        
        # Create research data format
        research_data = {
            "topic": research_topic,
            "research_results": [{
                "topic": research_topic,
                "summary": research_summary
            }]
        }
        
        # Store it in session if available
        if session and hasattr(session, 'store_tool_output'):
            await session.store_tool_output("research_results", research_data)
    
    # Format research data for the report writer
    formatted_input = f"Create a simple business summary from the following research data:\n\n{json.dumps(research_data, indent=2)}"
    
    # Run the simple report sub-agent
    result = await Runner.run(simple_report_subagent, formatted_input)
    return result.final_output

@function_tool
async def research_report_tool(context: RunContextWrapper[CustomSession]) -> ResearchReportData:
    """Generate a comprehensive research report from research results using session context."""
    session = context.context
    
    # Get research results from session if available
    research_data = None
    if session and hasattr(session, 'get_tool_output'):
        research_data = await session.get_tool_output("research_results")
        
        # If no research_results, try latest_research
        if not research_data:
            latest_research = await session.get_tool_output("latest_research")
            if latest_research:
                # Convert to expected format
                research_data = {
                    "topic": latest_research.get("topic", "Research Topic"),
                    "research_results": [{
                        "topic": latest_research.get("topic", "Research Topic"),
                        "summary": latest_research.get("summary", "No summary available")
                    }]
                }
    
    # If still no research data, conduct research first
    if not research_data:
        # Get the research topic from recent conversation
        research_topic = "business analysis"
        if session:
            items = await session.get_items()
            if items:
                for item in reversed(items):
                    if hasattr(item, 'content') and item.content:
                        research_topic = str(item.content)[:200]
                        break
        
        # Conduct research first
        print("🔍 No research data found. Conducting comprehensive research first...")
        research_request = f"Search term: {research_topic}\nReason for searching: Research for comprehensive report generation"
        result = await Runner.run(research_subagent, research_request)
        research_summary = str(result.final_output) if result.final_output else "No research results found"
        
        # Create research data format
        research_data = {
            "topic": research_topic,
            "research_results": [{
                "topic": research_topic,
                "summary": research_summary
            }]
        }
        
        # Store it in session if available
        if session and hasattr(session, 'store_tool_output'):
            await session.store_tool_output("research_results", research_data)
    
    # Format research data for the report writer
    formatted_input = f"Create a comprehensive research report from the following research data:\n\n{json.dumps(research_data, indent=2)}"
    
    # Run the research report sub-agent
    result = await Runner.run(research_report_subagent, formatted_input)
    return result.final_output

research_agent = Agent(
    name="Research agent",
    instructions=INSTRUCTIONS,
    tools=[research_tool, simple_report_tool, research_report_tool],
    model="gpt-4o",
)

def extract_research_topics(research_plan: Dict[str, Any]) -> List[str]:
    """Extract all research topics from the research plan outline."""
    research_topics = []
    
    # Extract user requested research topics
    if "user_requested_research_topics" in research_plan:
        research_topics.extend(research_plan["user_requested_research_topics"])
    
    # Extract topics from research plan outline
    if "research_plan_outline" in research_plan:
        outline = research_plan["research_plan_outline"]
        for category, subcategories in outline.items():
            for subcategory, topics in subcategories.items():
                if isinstance(topics, list):
                    research_topics.extend(topics)
                else:
                    research_topics.append(f"{category}: {subcategory}")
    
    return research_topics

async def conduct_single_research(topic: str, research_plan_data: Dict[str, Any]) -> ResearchResult:
    """Conduct research for a single topic."""
    business_context = research_plan_data.get("business_context", {})
    main_topic = research_plan_data.get("topic", "")
    
    # Enhance the search query with business context
    search_query = f"{main_topic} {topic}"
    if business_context.get("industry"):
        search_query += f" {business_context['industry']}"
    if business_context.get("location"):
        search_query += f" {business_context['location']}"
    
    # Format the input correctly for the search agent
    search_input = f"Search term: {search_query}\nReason for searching: Research on {topic} for {main_topic}"
    
    print(f"🔍 Researching: {topic}")
    
    # Use the search agent
    result = await Runner.run(research_agent, search_input)
    
    return ResearchResult(
        topic=topic,
        search_query=search_query,
        summary=str(result.final_output) if result.final_output else "No results found"
    )

async def conduct_research_plan(research_plan_data: Dict[str, Any]) -> ResearchPlanResults:
    """Conduct research for all topics in the research plan."""
    # Extract all research topics
    research_topics = extract_research_topics(research_plan_data)
    
    # Conduct research for each topic
    research_results = []
    for topic in research_topics:
        result = await conduct_single_research(topic, research_plan_data)
        research_results.append(result)
    
    return ResearchPlanResults(
        topic=research_plan_data.get("topic", ""),
        business_context=research_plan_data.get("business_context", {}),
        research_results=research_results,
        completion_status="completed"
    )




