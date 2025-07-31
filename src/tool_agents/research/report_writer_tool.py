from agents import Agent, Runner, function_tool

from src.agent_memory import AGENT_MEMORY

RESEARCH_REPORT_PROMPT = """
    You are a business analyst creating a comprehensive research report. You will receive research 
    results from multiple topics and need to synthesize them into a structured, professional report.

    ResearchReportData structure:
    - executive_summary: A comprehensive executive summary (200-300 words)
    - full_report: The complete research report in markdown format
    - key_insights: List of 6-10 most important insights
    - recommendations: List of 6-10 specific actionable recommendations
    - follow_up_research: 5-7 areas needing additional research
    - research_gaps: 3-5 areas where research was insufficient

    REPORT STRUCTURE:
    1. Executive Summary (2-3 paragraphs)
    2. Key Findings (organized by topic)
    3. Market Analysis (synthesis of market data)
    4. Opportunities & Challenges
    5. Strategic Recommendations
    6. Implementation Roadmap
    7. Risk Assessment
    8. Conclusion

    REQUIREMENTS:
    - Keep the report comprehensive but focused (1000-1500 words)
    - Use professional business language
    - Include markdown formatting with headers and bullet points
    - Synthesize findings across all research areas
    - Provide specific, actionable recommendations
    - Highlight key statistics and trends
    - Connect insights to business objectives

    Do not include URLs or citations. Focus on synthesized insights and strategic analysis.

    
    Example:
    ```
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
    ```
    """

@function_tool
async def report_writer_tool() -> str:
    """Generate a comprehensive research report from research results using session context."""    
    
    report_writer = Agent(
        name="Report Writer Tool-Agent", 
        instructions=RESEARCH_REPORT_PROMPT,
        model="gpt-4o-mini",
    )
    # Get research results from session if available
    research_data = await AGENT_MEMORY.get_tool_output("research_tool")
        
    # Run the research report sub-agent
    result = await Runner.run(report_writer, research_data)
    return result.final_output