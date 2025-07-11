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
   git clone https://github.com/your-username/research-bot.git
   cd research-bot
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
OPENAI_BASE_URL=https://your-api-endpoint.com
OPENAI_API_KEY=your_api_key_here
OPENAI_AGENTS_DISABLE_TRACING=1
OPENAI_LOGGING_LEVEL=ERROR
AGENTS_LOGGING_LEVEL=ERROR
```

### API Key Security

- The `.env` file is automatically ignored by git
- Never commit your actual API keys
- Use environment variables for sensitive data

## Usage

1. **Start the bot**: `./run.sh`
2. **Enter your research query**: The bot will ask what you want to research
3. **Watch the progress**: See real-time updates as the bot plans searches, performs them, and generates reports
4. **Get your report**: Receive a comprehensive markdown report with follow-up questions

## Project Structure

```
research_bot/
├── agents/                 # Agent definitions
│   ├── planner_agent.py   # Plans search strategy
│   ├── search_agent.py    # Performs web searches
│   └── writer_agent.py    # Generates reports
├── main.py                # Entry point
├── manager.py             # Orchestrates the research process
└── printer.py             # Rich console output
```

## Development

### Setup Development Environment

```bash
# Install with development dependencies
uv sync --group dev

# Run tests
uv run pytest

# Format code
uv run black research_bot/
uv run isort research_bot/

# Type checking
uv run mypy research_bot/
```

### Adding New Features

1. **New Agents**: Add agent definitions in `research_bot/agents/`
2. **New Tools**: Extend the agents with additional tools
3. **UI Improvements**: Modify `printer.py` for different output formats

## Dependencies

- **openai-agents**: OpenAI Agents SDK for AI-powered research
- **rich**: Beautiful console output and progress tracking
- **pydantic**: Data validation and model definitions
- **python-dotenv**: Environment variable management

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Run tests: `uv run pytest`
5. Commit your changes: `git commit -am 'Add feature'`
6. Push to the branch: `git push origin feature-name`
7. Submit a pull request

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [OpenAI Agents SDK](https://github.com/openai/openai-agents-python)
- Console interface powered by [Rich](https://rich.readthedocs.io/)
- Project structure inspired by modern Python packaging standards 