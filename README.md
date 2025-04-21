# Merlin

Merlin is an autonomous AI agent that can control your computer through natural language commands. Powered by OpenAI's models, it can execute terminal commands, search for files, and assist with various tasks.

## Features

- Execute shell commands through natural language instructions
- Search for files using fuzzy matching
- Maintain conversation context for complex multi-step tasks
- Configurable to access only specific directories for security
- Custom system prompts to define the agent's capabilities

## Requirements

- Python 3.12+
- OpenAI API key

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/merlin.git
cd merlin
```

2. Create a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate
```

3. Install the dependencies:

```bash
pip install -r requirements.txt
```

4. Create your `.env` file by copying the example:

```bash
cp .env.example .env
```

5. Edit the `.env` file with your configuration:
   - Add your OpenAI API key
   - Configure directories you want Merlin to access
   - Adjust other settings as needed

## Configuration

The `.env` file contains several important settings:

```
# Required configuration
OPENAI_API_KEY="your-openai-api-key-here"

# Directory configuration (where Merlin can access)
MERLIN_DIR_HOME=/path/to/your/home
MERLIN_DIR_WORK=/path/to/your/project

# Additional configuration
MODEL_NAME="gpt-4o"  # OpenAI model to use
SYSTEM_PROMPT=""  # Custom system prompt (will use default if empty)
FUZZY_SEARCH_THRESHOLD=60  # Fuzzy search matching threshold
DEFAULT_SEARCH_RESULTS=3  # Default number of search results
```

**Security Note**: For safety, Merlin can only access directories that you explicitly configure with the `MERLIN_DIR_` prefix. The current working directory is always accessible.

## Usage

Start Merlin by running:

```bash
python main.py
```

You'll see a prompt where you can type your commands:

```
- Using model: gpt-4o
- Using default system prompt
- Agent has access to 2 directories:
  - home: /path/to/your/home
  - cwd: /current/working/directory
- Type 'exit' or press Ctrl+C to quit
>>>
```

Example commands:

```
>>> List all Python files in the current directory
>>> Create a new directory called 'test' and create a simple Python script in it
>>> What's the current date and time?
>>> How much disk space do I have left?
```

Type `exit` or press `Ctrl+C` to quit.

## Project Structure

```
merlin/
├── .env                  # Configuration file
├── main.py               # Entry point
├── src/
│   ├── agent/            # Agent implementation
│   │   ├── agent_state.py     # State management
│   │   └── openai_agent.py    # OpenAI integration
│   ├── tools/            # Tool implementations
│   │   ├── command_executor.py # Shell command execution
│   │   ├── directory_manager.py # Directory management
│   │   └── vector_search.py     # File search functionality
│   └── utils/            # Utilities
│       ├── config.py          # Configuration loading
│       └── tools_config.py    # Tool definitions
└── tests/                # Test suite
```

## License

[License information here]

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

This project was inspired by various AI agent frameworks and personal assistant tools.
