---
name: python
description: Write, review, and debug Python code following idiomatic style, typing, and packaging conventions used in this repo (uv, pyproject.toml, Python 3.14+). Use when the user asks to write/modify Python scripts, fix a Python bug, design a module/class, add type hints, or set up dependencies with uv.
metadata:
  type: language
  language: python
---

# Python Skill

## When to Use
- The user asks to write, review, refactor, or debug Python code.
- The task involves designing functions/classes/modules in this repo.
- The task involves dependency management via `uv` / `pyproject.toml`.
- The task involves writing or updating Jupyter notebook cells (`.ipynb`) in Python.

## How to Use
1. Read `INSTRUCTIONS.md` for conventions, style rules, and the standard workflow to follow before writing code.
2. Read `EXAMPLES.md` for worked examples showing the expected shape of idiomatic code, typing, and error handling in this codebase.
3. Apply the conventions directly — don't just describe them, write the code accordingly.

## Quick Reference
- Python version: 3.14+
- Package manager: `uv` (`uv sync`, `uv add <pkg>`, `uv run <cmd>`)
- Prefer standard library and already-installed dependencies over adding new ones.
- Type hints are expected on function signatures for non-trivial code.
- No unused imports, no dead code, no speculative abstractions.
