"""Builds the deep agent used by the Streamlit chatbot.

Everything configurable here maps 1:1 to a feature demonstrated in the
deepagent notebooks:

- `1-basicdeepagent.ipynb`  -> model + web_search tool + system prompt, planning,
                               the virtual filesystem exposed via `result["files"]`
- `2-contextengineering.ipynb` -> system prompt as input context, AGENTS.md as
                               durable memory, skills as memory context,
                               CodeInterpreterMiddleware, subagents
- `3-backends.ipynb`        -> StateBackend / FilesystemBackend / StoreBackend
- `subagents.ipynb`         -> custom subagents, per-subagent model, and a
                               subagent with structured output (`response_format`)
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal

from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend, StateBackend, StoreBackend
from deepagents.backends.utils import create_file_data
from langchain.agents.structured_output import ToolStrategy
from langgraph.checkpoint.memory import MemorySaver
from langgraph.store.memory import InMemoryStore
from pydantic import BaseModel, Field

# The notebooks use paths relative to the deepagent/ folder ("projects/AGENTS.md",
# "skills/langgraph/SKILL.md"), so anchor everything to that folder.
DEEPAGENT_DIR = Path(__file__).resolve().parent.parent
AGENTS_MD_PATH = DEEPAGENT_DIR / "projects" / "AGENTS.md"
SKILLS_DIR = DEEPAGENT_DIR / "skills"

# Virtual paths the agent sees, regardless of which backend stores them.
AGENTS_MD_VPATH = "/projects/AGENTS.md"
SKILLS_VPATH = "/skills/"

BackendName = Literal["StateBackend", "FilesystemBackend", "StoreBackend"]

# Verified against this project's keys; the notebooks use the first three.
MODELS: dict[str, str] = {
    "groq:openai/gpt-oss-120b": "GROQ_API_KEY",
    "groq:openai/gpt-oss-20b": "GROQ_API_KEY",
    "groq:qwen/qwen3.6-27b": "GROQ_API_KEY",
    "groq:qwen/qwen3.8-27b": "GROQ_API_KEY",
    "groq:openai/gpt-oss-safeguard-20b": "GROQ_API_KEY",
    # Mistral ids need the explicit provider prefix: only "mistral-*" is
    # auto-inferred, so bare "ministral-*"/"codestral-*" raise
    # "Unable to infer model provider".
    "mistralai:mistral-small-latest": "MISTRAL_API_KEY",
    "mistralai:ministral-8b-latest": "MISTRAL_API_KEY",
    "mistralai:ministral-3b-latest": "MISTRAL_API_KEY",
    "mistralai:ministral-14b-latest": "MISTRAL_API_KEY",
    "mistralai:codestral-latest": "MISTRAL_API_KEY",
}

DEFAULT_SYSTEM_PROMPT = (
    "You are a research assistant specializing in scientific literature. "
    "Always cite sources. Use subagents for parallel research on different topics. "
    # Without this, a multi-step request gets delegated straight to a subagent and
    # no plan is ever recorded in the main agent's state (subagents have their own
    # middleware stack, so their planning is invisible here).
    "For any request needing three or more steps, call `write_todos` FIRST to "
    "record the plan, then do the work -- delegating to subagents if useful -- and "
    "mark each todo completed as you finish it."
)

BACKEND_HELP: dict[BackendName, str] = {
    "StateBackend": "Files live in LangGraph state (RAM, one thread). Ephemeral scratch space.",
    "FilesystemBackend": "Files live on real disk under root_dir. Survives restarts.",
    "StoreBackend": "Files live in a LangGraph store, scoped by namespace. Shared across threads.",
}


# --------------------------------------------------------------------------- #
# Tools
# --------------------------------------------------------------------------- #
def web_search(
    query: str,
    max_results: int = 5,
    topic: Literal["general", "sports", "news", "finance"] = "general",
    include_raw_content: bool = False,
) -> dict[str, Any]:
    """Run a web search."""
    from tavily import TavilyClient

    client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    return client.search(
        query,
        max_results=max_results,
        include_raw_content=include_raw_content,
        topic=topic,
    )


class ResearchFindings(BaseModel):
    """Structured findings from a research task."""

    summary: str = Field(description="Summary of findings")
    confidence: float = Field(description="Confidence score from 0 to 1")
    sources: list[str] = Field(description="List of source URLs")


def build_subagents(model: str, *, include_structured: bool = False) -> list[dict[str, Any]]:
    """Specialised subagents, so the main agent can delegate for context isolation.

    Mirrors `subagents.ipynb`: a tool-using subagent with an explicit
    per-subagent `model`, plus an optional structured-output subagent.

    `include_structured` is off by default because it is provider-dependent -- see
    the `researcher` entry below.
    """
    subagents: list[dict[str, Any]] = [
        {
            "name": "research-agent",
            "description": (
                "Researches a single topic in depth using web search. "
                "Spawn several in parallel to cover different topics."
            ),
            "system_prompt": (
                "You research one narrow topic thoroughly and report back concise, "
                "cited findings. Always include source URLs."
            ),
            "tools": [web_search],
            # Subagents can run their own model; default to the main one so the
            # sidebar selection stays authoritative.
            "model": model,
        },
        {
            "name": "report-writer",
            "description": (
                "Turns raw research notes into a structured, readable report. "
                "Use after research is gathered."
            ),
            "system_prompt": (
                "You write clear, well-structured reports from supplied notes. "
                "Use headings and keep every claim traceable to its source."
            ),
        },
    ]

    if include_structured:
        # `subagents.ipynb` pairs a subagent with a Pydantic `response_format`.
        # Provider-dependent in practice: deepagents always gives a subagent
        # filesystem tools, and Groq rejects native JSON mode combined with tool
        # calling, while ToolStrategy's forced tool_choice is not honoured by the
        # gpt-oss / qwen models. Works on providers that allow both.
        subagents.append(
            {
                "name": "researcher",
                "description": (
                    "Researches a topic and returns structured findings "
                    "(summary, confidence, sources)."
                ),
                "system_prompt": "Research the given topic thoroughly. Return your findings.",
                "tools": [web_search],
                "response_format": ToolStrategy(ResearchFindings),
            }
        )

    return subagents


# --------------------------------------------------------------------------- #
# Context files (AGENTS.md memory + skills)
# --------------------------------------------------------------------------- #
def load_agents_md() -> str | None:
    """Read the AGENTS.md operating context, if it exists on disk."""
    if AGENTS_MD_PATH.exists():
        return AGENTS_MD_PATH.read_text(encoding="utf-8")
    return None


def available_skills() -> list[str]:
    """Skill folder names that actually contain a SKILL.md."""
    if not SKILLS_DIR.exists():
        return []
    return sorted(
        d.name for d in SKILLS_DIR.iterdir() if d.is_dir() and (d / "SKILL.md").exists()
    )


def build_context_files(*, use_skills: bool, use_memory: bool) -> dict[str, Any]:
    """Virtual-path -> FileData map used to seed StateBackend / StoreBackend.

    FilesystemBackend needs none of this: the files are already on disk.
    """
    files: dict[str, Any] = {}

    if use_memory:
        agents_md = load_agents_md()
        if agents_md is not None:
            files[AGENTS_MD_VPATH] = create_file_data(agents_md)

    if use_skills:
        for name in available_skills():
            # Seed every markdown file in the skill so the agent can drill past
            # SKILL.md into INSTRUCTIONS.md / EXAMPLES.md with read_file.
            for md in sorted((SKILLS_DIR / name).glob("*.md")):
                vpath = f"/skills/{name}/{md.name}"
                files[vpath] = create_file_data(md.read_text(encoding="utf-8"))

    return files


# --------------------------------------------------------------------------- #
# Agent configuration
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class AgentConfig:
    """Everything the sidebar can change. Used as the agent's cache key."""

    model: str = next(iter(MODELS))
    backend: BackendName = "StateBackend"
    system_prompt: str = DEFAULT_SYSTEM_PROMPT
    use_web_search: bool = True
    use_skills: bool = True
    use_memory: bool = True
    use_subagents: bool = True
    use_planning: bool = True
    use_structured_subagent: bool = False
    use_code_interpreter: bool = False


@dataclass
class BuiltAgent:
    """A compiled agent plus the bits the UI needs to inspect or seed it."""

    agent: Any
    config: AgentConfig
    seed_files: dict[str, Any] = field(default_factory=dict)
    store: InMemoryStore | None = None
    filesystem_root: Path | None = None
    notes: list[str] = field(default_factory=list)


def build_agent(cfg: AgentConfig, *, store: InMemoryStore | None = None) -> BuiltAgent:
    """Compile a deep agent for the given configuration.

    `store` is passed in (not created here) so it can live in the Streamlit
    session and outlive agent rebuilds -- that is what makes StoreBackend files
    survive across threads.
    """
    notes: list[str] = []
    context_files = build_context_files(use_skills=cfg.use_skills, use_memory=cfg.use_memory)

    tools = [web_search] if cfg.use_web_search else []
    if cfg.use_web_search and not os.getenv("TAVILY_API_KEY"):
        notes.append("TAVILY_API_KEY is not set - web_search will fail if called.")

    middleware = []
    if cfg.use_planning:
        # deepagents 0.7 does not add this by default: it supplies the
        # `write_todos` tool and the `todos` state channel the Plan tab reads.
        from langchain.agents.middleware import TodoListMiddleware

        middleware.append(TodoListMiddleware())

    if cfg.use_code_interpreter:
        try:
            from langchain_quickjs import CodeInterpreterMiddleware

            middleware.append(CodeInterpreterMiddleware())
        except Exception as exc:  # pragma: no cover - depends on optional install
            notes.append(f"Code interpreter unavailable: {exc}")

    # `memory=` only makes sense if AGENTS.md is actually reachable for this backend.
    memory: list[str] | None = None
    if cfg.use_memory and AGENTS_MD_PATH.exists():
        memory = [AGENTS_MD_VPATH]
    elif cfg.use_memory:
        notes.append(f"No AGENTS.md at {AGENTS_MD_PATH} - memory disabled.")

    skills: list[str] | None = None
    if cfg.use_skills and available_skills():
        skills = [SKILLS_VPATH]
    elif cfg.use_skills:
        notes.append(f"No skills found under {SKILLS_DIR} - skills disabled.")

    kwargs: dict[str, Any] = {
        "model": cfg.model,
        "tools": tools,
        "system_prompt": cfg.system_prompt,
        "middleware": middleware,
        "skills": skills,
        "memory": memory,
        "checkpointer": MemorySaver(),
    }
    if cfg.use_subagents:
        kwargs["subagents"] = build_subagents(
            cfg.model, include_structured=cfg.use_structured_subagent
        )

    seed_files: dict[str, Any] = {}
    active_store: InMemoryStore | None = None
    fs_root: Path | None = None

    if cfg.backend == "StateBackend":
        kwargs["backend"] = StateBackend()
        # State files must be seeded with the first message of each thread.
        seed_files = context_files

    elif cfg.backend == "FilesystemBackend":
        fs_root = DEEPAGENT_DIR
        # virtual_mode keeps the agent inside root_dir (no '..' escapes).
        kwargs["backend"] = FilesystemBackend(root_dir=str(fs_root), virtual_mode=True)
        notes.append(f"Agent has real read/write access under {fs_root}.")

    elif cfg.backend == "StoreBackend":
        active_store = store if store is not None else InMemoryStore()
        namespace = ("memories",)
        # Seed durable context into the store once; keys are the virtual paths.
        for vpath, data in context_files.items():
            if active_store.get(namespace, vpath) is None:
                active_store.put(namespace, vpath, data)
        kwargs["backend"] = StoreBackend(store=active_store, namespace=lambda _rt: namespace)
        kwargs["store"] = active_store

    else:  # pragma: no cover - guarded by the UI
        raise ValueError(f"Unknown backend: {cfg.backend}")

    agent = create_deep_agent(**kwargs)
    return BuiltAgent(
        agent=agent,
        config=cfg,
        seed_files=seed_files,
        store=active_store,
        filesystem_root=fs_root,
        notes=notes,
    )


# --------------------------------------------------------------------------- #
# Reading files back out of whichever backend is active
# --------------------------------------------------------------------------- #
def list_backend_files(built: BuiltAgent, state_values: dict[str, Any] | None) -> dict[str, str]:
    """Virtual path -> text content, read from the backend that is in use."""
    cfg = built.config

    if cfg.backend == "StateBackend":
        files = (state_values or {}).get("files") or {}
        return {path: _file_text(data) for path, data in files.items()}

    if cfg.backend == "StoreBackend" and built.store is not None:
        items = built.store.search(("memories",), limit=200)
        return {str(item.key): _file_text(item.value) for item in items}

    if cfg.backend == "FilesystemBackend" and built.filesystem_root is not None:
        return _read_disk_tree(built.filesystem_root)

    return {}


def _file_text(data: Any) -> str:
    """FileData (or a store value) -> displayable text."""
    if isinstance(data, dict):
        content = data.get("content", "")
    else:
        content = data
    if isinstance(content, list):
        content = "".join(str(part) for part in content)
    return str(content)


def _read_disk_tree(root: Path, *, max_files: int = 60, max_bytes: int = 40_000) -> dict[str, str]:
    """Shallow view of real files under root, for the Files tab."""
    skip_dirs = {".venv", ".git", "__pycache__", ".ipynb_checkpoints", ".claude"}
    out: dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        if len(out) >= max_files:
            break
        if not path.is_file() or path.suffix in {".ipynb", ".lock"}:
            continue
        if any(part in skip_dirs for part in path.relative_to(root).parts):
            continue
        vpath = "/" + path.relative_to(root).as_posix()
        try:
            if path.stat().st_size > max_bytes:
                out[vpath] = f"<{path.stat().st_size} bytes - too large to preview>"
            else:
                out[vpath] = path.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            out[vpath] = f"<unreadable: {exc}>"
    return out
