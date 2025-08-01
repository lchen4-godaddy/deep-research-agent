# Test Suite for Deep Research Agent

This directory contains comprehensive tests for all tool_agents and tools in the Deep Research Agent system.

## Test Structure

### Tool Agents Tests

#### Planner Tool Agents
- `tool_agents/planner/test_plan_writer_tool.py` - Tests the plan writer tool that creates research plans
- `tool_agents/planner/test_plan_summarizer_tool.py` - Tests the plan summarizer tool

#### Research Tool Agents
- `tool_agents/research/test_research_tool.py` - Tests the main research tool that orchestrates research
- `tool_agents/research/test_query_writer_tool.py` - Tests the query writer tool that generates search queries
- `tool_agents/research/test_contextual_summary_tool.py` - Tests the contextual summary tool
- `tool_agents/research/test_report_writer_tool.py` - Tests the report writer tool

### Tools Tests

#### Core Tools
- `tools/test_researcher.py` - Tests the main researcher tool
- `tools/test_web_search_tool.py` - Tests the web search tool with mock and real data
- `tools/web_scraper/test_web_scraper.py` - Tests the web scraper tool (existing)

## Running Tests

### Run All Tests
```bash
python tests/run_all_tests.py
```

### Run Specific Test Categories
```bash
# Run only planner tool tests
python tests/run_all_tests.py planner

# Run only research tool tests
python tests/run_all_tests.py research

# Run only web search tests
python tests/run_all_tests.py web_search
```

### Run Individual Tests
```bash
# Run specific tool agent tests
python tests/tool_agents/planner/test_plan_writer_tool.py
python tests/tool_agents/research/test_research_tool.py

# Run specific tool tests
python tests/tools/test_web_search_tool.py
python tests/tools/test_researcher.py
```

## Test Features

### LLM Integration Tests
All tool_agents tests include LLM calls for human validation. These tests:
- Call the actual LLM once per test
- Print the output for human review
- Include clear validation prompts
- Handle errors gracefully

### Mock Tests
Some tools include mock tests for faster development:
- `test_web_search_tool.py` includes mock tests for the source_finder function
- Web scraper tests include both unit and integration tests

### Test Data
Tests use realistic test data:
- Business scenarios (organic coffee business, AI research tools)
- Realistic research questions
- Structured test plans and data

## Test Output Format

Each test provides:
1. **Input Context** - What the test is testing
2. **LLM Output** - The actual output from the LLM
3. **Validation Prompt** - Clear instructions for human validation
4. **Error Handling** - Graceful error reporting with stack traces

## Environment Requirements

Tests require:
- `.env` file with API keys
- Internet connection for web search tests
- All dependencies installed (`uv install`)

## Test Categories

### Tool Agents (LLM Tests)
These tests call the LLM and require human validation:

1. **Plan Writer Tool** - Creates research plans from conversation context
2. **Plan Summarizer Tool** - Summarizes research plans
3. **Research Tool** - Orchestrates research using the research plan
4. **Query Writer Tool** - Generates search queries from research questions
5. **Contextual Summary Tool** - Summarizes content in context of research questions
6. **Report Writer Tool** - Generates comprehensive research reports

### Tools (Functional Tests)
These tests focus on functionality:

1. **Researcher Tool** - Main research orchestration
2. **Web Search Tool** - Web search and summarization
3. **Web Scraper Tool** - Web content extraction

## Validation Guidelines

When reviewing LLM test outputs, consider:

1. **Relevance** - Does the output address the input question/context?
2. **Completeness** - Does it cover all required aspects?
3. **Quality** - Is the output well-structured and informative?
4. **Accuracy** - Are the facts and information correct?
5. **Clarity** - Is the output clear and easy to understand?

## Troubleshooting

### Common Issues

1. **Import Errors** - Ensure the src directory is in the Python path
2. **API Key Errors** - Check that your `.env` file contains valid API keys
3. **Network Errors** - Some tests require internet connectivity
4. **Memory Errors** - Clear agent memory between tests if needed

### Debug Mode
To run tests with more verbose output, modify the test files to include additional print statements or use Python's logging module.

## Contributing

When adding new tests:
1. Follow the existing naming convention
2. Include both LLM tests (for tool_agents) and functional tests (for tools)
3. Add the test to the `run_all_tests.py` script
4. Update this README with new test descriptions 