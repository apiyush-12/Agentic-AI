# Python Skill — Instructions

## Style Conventions
- Follow PEP 8. Use 4-space indentation, `snake_case` for functions/variables, `PascalCase` for classes, `UPPER_SNAKE_CASE` for constants.
- Add type hints to all function/method signatures (parameters and return type). Use `from __future__ import annotations` when it simplifies forward references.
- Prefer f-strings for string formatting.
- Keep functions small and single-purpose. Extract a helper only when logic is reused or a function grows hard to read in one screen.
- Use `pathlib.Path` instead of `os.path` for filesystem paths.
- Use context managers (`with`) for files, sockets, and other resources that need cleanup.

## Error Handling
- Only catch exceptions you can meaningfully handle or that need translation into a clearer error at a boundary (CLI entry point, API handler).
- Don't swallow exceptions silently — re-raise or log with context if caught.
- Prefer raising specific exception types (`ValueError`, `TypeError`, custom exceptions) over bare `Exception`.
- Avoid defensive checks for conditions that can't occur given the code's own guarantees (e.g., re-validating an argument that a type hint already constrains).

## Dependency Management (uv)
- This repo uses `uv` with `pyproject.toml` as the single source of truth for dependencies.
- To add a dependency: `uv add <package>`. To add a dev-only dependency: `uv add --dev <package>`.
- To install/sync all dependencies: `uv sync`.
- To run a script or command inside the project's virtual environment: `uv run python script.py` or `uv run <tool>`.
- Never hand-edit the lockfile; let `uv` manage it.
- Don't introduce a new dependency for something the standard library or an existing dependency already covers.

## Working with Jupyter Notebooks in This Repo
- Notebooks live under `deepagent/` and `updatedlangchain/`; they are the primary code artifacts, not `.py` modules.
- When editing notebook cells, keep cell outputs consistent with the code (don't leave stale outputs implying different behavior).
- Load API keys via `python-dotenv` (`from dotenv import load_dotenv; load_dotenv()`) — never hardcode secrets in a cell.
- Keep notebook narrative (markdown cells) in sync with code cells when code changes meaningfully.

## Workflow Before Writing Code
1. Check whether similar functionality already exists in the repo (search before writing new code).
2. Confirm the Python version and available dependencies (`pyproject.toml`) before using a language feature or library.
3. Write the minimal code that satisfies the request — no speculative configuration flags, no unused parameters.
4. If the change is testable, verify it runs (`uv run python -c "..."` or execute the relevant notebook cell) before reporting done.

## Testing & Verification
- If a `tests/` directory or `pytest` config exists, run `uv run pytest` after changes touching testable code.
- For notebook-only changes, execute the modified cells to confirm they run without error and produce the expected output.
