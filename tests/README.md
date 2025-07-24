# Tests

This directory contains tests for the deep-research-agent project.

## Import Setup

The test files are configured to import from the `src` directory using the `src.` prefix. This is handled automatically by the `conftest.py` file in this directory.

### How it works

1. **conftest.py**: This file adds the project root to the Python path, allowing imports with the `src.` prefix
2. **Import pattern**: All test files should use imports like:
   ```python
   from src.tools.web_search_tool import web_search
   from src.main_agents.research_agent import research_agent
   from src.tool_agents.research.research_tool import research_tool
   ```

### Why this approach?

- The project is designed to be run as a module (`python -m src.main`)
- The source code uses relative imports (e.g., `from ..tool_agents.research.research_tool import research_tool`)
- Adding the project root to the Python path allows the relative imports to work correctly
- This approach maintains consistency with how the project is intended to be run

## Running Tests

```bash
# Run all tests
uv run pytest

# Run specific test file
uv run pytest tests/tools/test_web_search.py

# Run tests with verbose output
uv run pytest -v

# Run tests in a specific directory
uv run pytest tests/tools/
```

## Test Structure

- `tests/tools/`: Tests for the tools module (web search, scraping)
- `tests/main_agents/`: Tests for the main agents (structure only, no API calls)
- `tests/tool_agents/`: Tests for the tool agents
- `conftest.py`: Pytest configuration for imports and shared fixtures

## What We Test vs What We Skip

### ✅ **What We Test:**
- **Web Search Tools**: Real DDGS API calls to verify search functionality
- **Web Scraping**: Real HTTP requests to verify content extraction
- **Data Structures**: Agent configurations and tool setups
- **Error Handling**: How components handle failures gracefully

### ❌ **What We Skip:**
- **OpenAI API Calls**: Manager and agent execution tests to avoid costs
- **Complex Integration**: End-to-end workflows that require multiple API calls
- **Performance Tests**: Large-scale operations that could be expensive

## Test Design Principles

### 1. **Mock External Dependencies**
- **DDGS Search**: All tests mock the DuckDuckGo search to avoid real network calls
- **Web Scraping**: HTTP requests are mocked to avoid hitting real websites
- **AI Agents**: OpenAI API calls are mocked to avoid costs and ensure consistent results

### 2. **Test Structure Over Content**
- **Dynamic Results**: Tests verify data structure and types, not specific content
- **URL Validation**: Ensure URLs are valid HTTP/HTTPS links
- **Content Presence**: Verify content exists but don't assert specific text

### 3. **Error Scenarios**
- **Network Failures**: Test behavior when external services fail
- **Rate Limiting**: Test graceful handling of API limits
- **Invalid Inputs**: Test edge cases like empty queries or malformed URLs

### 4. **Integration Testing**
- **Agent Interactions**: Test how different agents work together
- **Data Flow**: Verify data passes correctly between components
- **Session Management**: Test session data persistence and retrieval 