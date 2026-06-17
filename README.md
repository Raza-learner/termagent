# AI Agent

An AI-powered coding agent that uses Google Gemini to autonomously explore, edit, and run Python code through function calling.

## Overview

This project connects to Google's Gemini API (`gemini-2.5-flash`) and provides the model with four tools it can use to interact with a codebase:

- **`get_files_info`** – List files in a directory
- **`get_file_content`** – Read file contents
- **`write_file`** – Create or overwrite files
- **`run_python_file`** – Execute Python scripts

The agent runs in a loop — calling Gemini, executing any function calls it makes, and feeding results back — up to 20 iterations per session.

## Usage

```bash
# Clone the repo
git clone https://github.com/yourusername/ai-agent.git
cd ai-agent

# Create a virtual environment (recommended)
python -m venv .venv && source .venv/bin/activate

# Install dependencies
pip install -e .

# Or using uv (faster)
uv sync

# Configuration
# 1. Copy the example env file
cp .env.example .env

# 2. Edit .env and add your Gemini API key:
#    GEMINI_API_KEY="your-api-key-here"

# 3. Or set it directly as an environment variable
export GEMINI_API_KEY="your-api-key-here"

# Run the agent with a prompt
python main.py "Fix the bug in calculator/math_ops.py"
python main.py "Run the calculator tests and report the results" --verbose
```

### Arguments

| Argument | Description |
|----------|-------------|
| `user_prompt` | The task prompt for the AI agent |
| `--verbose` | Show token usage and detailed function call info |

## Project Structure

```
.
├── main.py                  # Entry point – CLI + Gemini loop
├── config.py                # System prompt & constants
├── call_function.py         # Routes Gemini function calls to implementations
├── functions/
│   ├── get_files_info.py    # Directory listing tool
│   ├── get_file_content.py  # File reading tool
│   ├── write_file.py        # File writing tool
│   └── run_python_file.py   # Python execution tool
└── calculator/              # Testbed project for the agent
    ├── main.py              # CLI calculator (shunting-yard expression evaluator)
    ├── tests.py             # Unit tests for the calculator
    ├── math_ops.py          # Small test file for debugging
    ├── fix_bug.py           # Small test file for debugging
    └── pkg/
        ├── calculator.py    # Calculator class (infix evaluation)
        └── render.py        # JSON output formatting
```

## How It Works

1. The user provides a prompt via CLI.
2. The system prompt instructs Gemini it is a coding agent with access to the four tools.
3. Gemini responds with either a text answer or function calls.
4. If function calls are made, they are executed locally with a fixed `working_directory` of `./calculator`.
5. Results are sent back to Gemini for the next iteration.
6. The loop continues until Gemini responds with plain text (up to 20 rounds).

## Path Safety

All file tools validate that requested paths stay within the permitted working directory using `os.path.commonpath` — preventing directory traversal attacks.

## Dependencies

- Python >= 3.13
- `google-genai` – Gemini API client
- `pydantic` – Data validation
- `python-dotenv` – Environment variable loading

## Roadmap

- [ ] Interactive TUI (like opencode CLI) — browse files, preview diffs, approve/reject changes
- [ ] Multi-file editing and refactoring workflows
- [ ] Support for additional LLM providers (Claude, GPT, etc.)
- [ ] Configurable working directory (not hardcoded to `./calculator`)
- [ ] Sandboxed execution environment
- [ ] Git integration — auto-commit, branch management, PR creation

> **Note:** This project is actively being improved. A terminal UI (TUI) similar to [opencode CLI](https://opencode.ai) is in the works for a more interactive coding agent experience.

## License

MIT
