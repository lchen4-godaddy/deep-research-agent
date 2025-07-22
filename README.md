# Deep Research Agent for Business Development

A deep research assistant that creates a comprehensive research report for your business or product idea.

## Features

- **Intelligent Search Planning**: Uses AI to plan multiple targeted web searches
- **Web Search Integration**: Performs actual web searches using OpenAI's agents
- **Report Generation**: Creates detailed markdown reports with summaries and follow-up questions
- **Rich Console Interface**: Beautiful progress tracking with spinners and status updates
- **Error Handling**: Graceful handling of API errors and network issues
- **Multi-Agent Architecture**: Specialized agents for planning, research, clarification, and triage

## Quick Start

### Prerequisites

- Python 3.9-3.12
- OpenAI API key (or compatible API endpoint)
- [uv](https://docs.astral.sh/uv/) package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/lchen4-godaddy/deep-research-agent.git
   cd deep-research-agent
   ```

2. **Set up virtual environment and install dependencies**
   ```bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv sync
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API key and configuration
   ```

4. **Run the deep research agent**
   ```bash
   ./run.sh
   ```

## Development Setup

### Install uv
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Set up development environment
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv sync --group dev
```

### Run tests (NOT FUNCTIONAL)
```bash
uv run pytest
```

### Run linting
```bash
uv run ruff check .
uv run black .
```

## Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
GOCODE_API_TOKEN='your-api-key'
OPENAI_BASE_URL=https://caas-gocode-prod.caas-prod.prod.onkatana.net
OPENAI_API_KEY=${GOCODE_API_TOKEN}
OPENAI_AGENTS_DISABLE_TRACING=1
OPENAI_LOGGING_LEVEL=ERROR
AGENTS_LOGGING_LEVEL=ERROR
```

### API Key Security

- The `.env` file is automatically ignored by git
- Never commit your actual API keys
- Use environment variables for sensitive data

## Project Structure

```
src/
├── agents/                    # Agent definitions
│   ├── planner_agent.py      # Plans search strategy
│   ├── research_agent.py     # Performs web searches and research
│   ├── clarification_agent.py # Handles user clarification
│   ├── triage_agent.py       # Evaluates and categorizes information
│   ├── search_plan_agent.py  # Creates detailed search plans
│   └── tools/                # Agent tools and utilities
├── main.py                   # Entry point
├── manager.py                # Orchestrates the research process
├── custom_session.py         # Custom session management
├── printer.py                # Rich console output
├── globals.py                # Global configuration
├── test_manager.py           # Testing utilities
├── example_user_context/     # Example user contexts
└── sample_outputs/           # Sample research outputs
```

## Architecture

The project uses a multi-agent architecture:

- **Planner Agent**: Creates high-level research strategies
- **Research Agent**: Performs web searches and gathers information
- **Clarification Agent**: Handles user questions and clarifications
- **Triage Agent**: Evaluates and categorizes gathered information
- **Search Plan Agent**: Creates detailed search execution plans

## Dependencies

- **openai-agents**: OpenAI Agents SDK for AI-powered research
- **rich**: Beautiful console output and progress tracking
- **pydantic**: Data validation and model definitions
- **python-dotenv**: Environment variable management
- **requests**: HTTP client for web requests
- **typing-extensions**: Enhanced type hints

## Development

### Adding New Features

1. **New Agents**: Add agent definitions in `src/agents/`
2. **New Tools**: Extend the agents with additional tools in `src/agents/tools/`
3. **UI Improvements**: Modify `src/printer.py` for different output formats
4. **Configuration**: Update `src/globals.py` for new settings

### Testing (NOT IMPLEMENTED, WIP)

The project includes comprehensive testing with pytest:

```bash
# Run all tests
uv run pytest

# Run specific test file
uv run pytest src/test_manager.py

# Run with coverage
uv run pytest --cov=src
```

### Code Quality

The project uses several tools for code quality:

- **ruff**: Fast Python linter
- **black**: Code formatting
- **isort**: Import sorting
- **mypy**: Type checking

Run all quality checks:

```bash
uv run ruff check .
uv run black .
uv run isort .
uv run mypy src/
```