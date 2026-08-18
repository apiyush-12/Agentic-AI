# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a LangChain v1.3.14 learning and reference repository containing Jupyter notebooks that demonstrate key concepts and integrations:
- `1-langchainintro.ipynb` — Agent basics and tool usage
- `2-modelintegration.ipynb` — LLM provider integrations
- `3-tools.ipynb` — Tool definitions and usage
- `4-messages.ipynb` — Message handling
- `5-structuredoutput.ipynb` — Structured output from LLMs

## Development Setup

**Python Version**: 3.14+

**Package Manager**: `uv` (configured in pyproject.toml)

**Key Commands**:
```bash
# Install dependencies
uv sync

# Run the main entry point
python -m langchainupdated

# Open and run notebooks (requires Jupyter)
jupyter notebook updatedlangchain/
```

## Dependencies & LLM Providers

The project integrates multiple LLM providers via LangChain Community packages:
- **OpenAI** — via `langchain-openai`
- **Groq** — via `langchain-groq`
- **Mistral AI** — via `langchain-mistralai`
- **Google GenAI** — via `langchain-google-genai`

Each provider requires its own API key stored in environment variables (managed via `.env` and `python-dotenv`).

## Code Structure

- **`updatedlangchain/`** — Jupyter notebooks (no Python modules)
- **`__init__.py`** — Minimal entry point with `main()` function
- **`pyproject.toml`** — Package config with uv and uv_build backend

The `uv` configuration specifies Windows-only environments (`sys_platform == 'win32'`).

## Important Notes

- This is primarily a notebook-based learning repository, not a typical Python package
- All interactive code examples are in `.ipynb` files; modify and test directly in Jupyter
- Environment variables (`.env` file) are required to authenticate with LLM providers
- The notebooks use LangChain v1, which has updated APIs compared to v0.x
