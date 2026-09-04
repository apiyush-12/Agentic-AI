# Python Skill — Examples

## Example 1: Typed function with clear error boundary

```python
from pathlib import Path


def load_config(path: Path) -> dict[str, str]:
    """Load key=value pairs from a config file."""
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    config: dict[str, str] = {}
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        key, _, value = line.partition("=")
        config[key.strip()] = value.strip()
    return config
```

## Example 2: Dataclass over ad-hoc dict

```python
from dataclasses import dataclass


@dataclass
class ToolResult:
    name: str
    output: str
    success: bool
```

Prefer this over passing around untyped `dict`s when the shape is fixed and known ahead of time.

## Example 3: uv dependency workflow

```bash
# Add a new runtime dependency
uv add httpx

# Add a dev-only dependency (e.g., testing)
uv add --dev pytest

# Sync environment to match pyproject.toml / lockfile
uv sync

# Run a script inside the managed environment
uv run python -m langchainupdated
```

## Example 4: Loading environment variables safely

```python
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ["OPENAI_API_KEY"]  # raises KeyError with a clear message if missing
```

Avoid `os.environ.get("OPENAI_API_KEY", "default-key")` for required secrets — fail loudly instead of silently using a placeholder.

## Example 5: Minimal, non-speculative function

```python
# Good — does exactly what's needed
def celsius_to_fahrenheit(celsius: float) -> float:
    return celsius * 9 / 5 + 32


# Avoid — unused flexibility nobody asked for
def celsius_to_fahrenheit(celsius: float, *, precision: int = 2, rounding_mode: str = "half-up") -> float:
    ...
```
