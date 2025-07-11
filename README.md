# Deep Research Agent

A research bot that uses AI agents to perform web searches and generate comprehensive reports.

## Features

- **Intelligent Search Planning**: Uses AI to plan multiple targeted web searches
- **Web Search Integration**: Performs actual web searches using OpenAI's agents
- **Report Generation**: Creates detailed markdown reports with summaries and follow-up questions
- **Rich Console Interface**: Beautiful progress tracking with spinners and status updates
- **Error Handling**: Graceful handling of API errors and network issues

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
2. **Set up virtual environment**
   ```bash
   uv venv
   source .venv/bin/activate
   ```

2. **Install dependencies**
   ```bash
   uv sync
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API key and configuration
   ```

4. **Run the research bot**
   ```bash
   ./run.sh
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
├── agents/                 # Agent definitions
│   ├── planner_agent.py   # Plans search strategy
│   ├── search_agent.py    # Performs web searches
│   └── writer_agent.py    # Generates reports
├── main.py                # Entry point
├── manager.py             # Orchestrates the research process
└── printer.py             # Rich console output
```

1. **New Agents**: Add agent definitions in `research_bot/agents/`
2. **New Tools**: Extend the agents with additional tools
3. **UI Improvements**: Modify `printer.py` for different output formats

## Dependencies

- **openai-agents**: OpenAI Agents SDK for AI-powered research
- **rich**: Beautiful console output and progress tracking
- **pydantic**: Data validation and model definitions
- **python-dotenv**: Environment variable management