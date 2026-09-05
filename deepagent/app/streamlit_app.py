"""Conversational Streamlit chatbot built on a deep agent.

Run it from the repo root:

    uv run streamlit run deepagent/app/streamlit_app.py

Features wired up (all drawn from the deepagent notebooks):
planning/todos, the virtual filesystem, subagents, skills, AGENTS.md memory,
swappable backends (State/Filesystem/Store), thread-scoped conversation memory
via a checkpointer, web search, and the QuickJS code interpreter.
"""

from __future__ import annotations

import os
import sys
import uuid
from pathlib import Path
from typing import Any

import streamlit as st
from dotenv import load_dotenv

# Streamlit runs this file as a script, so make the sibling module importable
# no matter which directory the server was started from.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from agent_factory import (
    BACKEND_HELP,
    DEFAULT_SYSTEM_PROMPT,
    MODELS,
    AgentConfig,
    BuiltAgent,
    available_skills,
    build_agent,
    list_backend_files,
    load_agents_md,
)
from langgraph.store.memory import InMemoryStore

load_dotenv()

st.set_page_config(page_title="Deep Agent Chat", page_icon="🧠", layout="wide")

TODO_ICONS = {"pending": "⬜", "in_progress": "🔄", "completed": "✅"}


# --------------------------------------------------------------------------- #
# Session state
# --------------------------------------------------------------------------- #
def init_state() -> None:
    st.session_state.setdefault("history", [])          # rendered chat turns
    st.session_state.setdefault("thread_id", str(uuid.uuid4()))
    st.session_state.setdefault("store", InMemoryStore())  # outlives agent rebuilds
    st.session_state.setdefault("built", None)
    st.session_state.setdefault("seeded_threads", set())
    st.session_state.setdefault("last_state", None)
    st.session_state.setdefault("last_todos", [])


def get_agent(cfg: AgentConfig) -> BuiltAgent:
    """Rebuild the agent only when the sidebar config actually changes."""
    built: BuiltAgent | None = st.session_state.built
    if built is None or built.config != cfg:
        built = build_agent(cfg, store=st.session_state.store)
        st.session_state.built = built
        # A rebuilt agent means a fresh checkpointer, so the thread must reseed.
        st.session_state.seeded_threads = set()
    return built


def new_thread() -> None:
    st.session_state.thread_id = str(uuid.uuid4())
    st.session_state.history = []
    st.session_state.last_state = None
    st.session_state.last_todos = []


# --------------------------------------------------------------------------- #
# Message helpers
# --------------------------------------------------------------------------- #
def message_text(message: Any) -> str:
    """Content of a message or chunk as plain text (providers differ in shape)."""
    content = getattr(message, "content", message)
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, str):
                parts.append(block)
            elif isinstance(block, dict) and block.get("type") == "text":
                parts.append(block.get("text", ""))
        return "".join(parts)
    return ""


def render_turn(turn: dict[str, Any]) -> None:
    """Render one assistant turn, including any error or fallback text."""
    render_events(turn.get("events") or [])

    # If nothing structured came back (e.g. the run failed mid-stream), fall back
    # to whatever text was streamed so the bubble is never silently empty.
    if not _has_answer(turn.get("events") or []) and turn.get("text", "").strip():
        st.markdown(turn["text"])

    if turn.get("error"):
        st.error(turn["error"])



def _has_answer(events: list[Any]) -> bool:
    return any(
        getattr(m, "type", None) == "ai" and message_text(m).strip() for m in events
    )


def render_events(events: list[Any]) -> None:
    """Render an agent turn: tool calls and results collapsed, answers inline."""
    for message in events:
        msg_type = getattr(message, "type", None)

        if msg_type == "ai":
            for call in getattr(message, "tool_calls", None) or []:
                with st.expander(f"🔧 {call.get('name', 'tool')}", expanded=False):
                    st.json(call.get("args", {}))
            text = message_text(message)
            if text.strip():
                st.markdown(text)

        elif msg_type == "tool":
            name = getattr(message, "name", "tool")
            with st.expander(f"↩️ result · {name}", expanded=False):
                text = message_text(message)
                st.code(text[:4000] + ("\n… truncated" if len(text) > 4000 else ""))


def stream_turn(built: BuiltAgent, user_text: str, config: dict) -> dict[str, Any]:
    """Invoke the agent, streaming tokens live and collecting structured events.

    Returns the turn record kept in history: structured `events`, the raw
    streamed `text` (fallback if the run dies mid-stream) and any `error`.
    """
    payload: dict[str, Any] = {"messages": [{"role": "user", "content": user_text}]}

    # StateBackend keeps files in thread state, so context files are seeded with
    # the first message of a thread only -- reseeding would clobber agent edits.
    if built.seed_files and st.session_state.thread_id not in st.session_state.seeded_threads:
        payload["files"] = built.seed_files
        st.session_state.seeded_threads.add(st.session_state.thread_id)

    events: list[Any] = []
    todos: list[Any] = []
    live = st.empty()
    buffer = ""

    try:
        for mode, chunk in built.agent.stream(
            payload, config=config, stream_mode=["updates", "messages"]
        ):
            if mode == "messages":
                message, _meta = chunk
                buffer += message_text(message)
                if buffer.strip():
                    live.markdown(buffer + "▌")
            elif mode == "updates" and isinstance(chunk, dict):
                for update in chunk.values():
                    if isinstance(update, dict):
                        events.extend(update.get("messages") or [])
                        # Capture the plan as it is written: a later state
                        # snapshot can miss it (e.g. work done inside a subagent).
                        if update.get("todos"):
                            todos = update["todos"]
    except Exception as exc:
        live.empty()
        return {
            "events": events,
            "text": buffer,
            "todos": todos,
            "error": f"Agent run failed: {exc}",
        }

    live.empty()  # replaced by the structured render below
    return {"events": events, "text": buffer, "todos": todos, "error": None}


# --------------------------------------------------------------------------- #
# Sidebar
# --------------------------------------------------------------------------- #
def sidebar() -> AgentConfig:
    st.sidebar.title("🧠 Deep Agent")

    st.sidebar.subheader("Model")
    model = st.sidebar.selectbox("Chat model", list(MODELS), index=0)
    required_key = MODELS[model]
    if not os.getenv(required_key):
        st.sidebar.error(f"{required_key} is not set in your .env")

    st.sidebar.subheader("Backend")
    backend = st.sidebar.radio(
        "Where files & memory live",
        list(BACKEND_HELP),
        index=0,
        help="From 3-backends.ipynb: the agent code is identical, only storage changes.",
    )
    st.sidebar.caption(BACKEND_HELP[backend])

    st.sidebar.subheader("Context engineering")
    use_memory = st.sidebar.toggle(
        "AGENTS.md memory",
        value=load_agents_md() is not None,
        help="Loads projects/AGENTS.md as durable operating context.",
    )
    skills = available_skills()
    use_skills = st.sidebar.toggle(
        f"Skills ({len(skills)})",
        value=bool(skills),
        help="Exposes /skills/ so the agent can pull in a skill on demand.",
    )
    if use_skills and skills:
        st.sidebar.caption(", ".join(skills))

    st.sidebar.subheader("Capabilities")
    use_web_search = st.sidebar.toggle("Web search (Tavily)", value=bool(os.getenv("TAVILY_API_KEY")))
    use_subagents = st.sidebar.toggle(
        "Subagents", value=True, help="research-agent + report-writer, for context isolation."
    )
    use_planning = st.sidebar.toggle(
        "Planning (todo list)", value=True, help="Adds write_todos; feeds the Plan tab."
    )
    use_structured_subagent = st.sidebar.toggle(
        "Structured-output subagent",
        value=False,
        disabled=not use_subagents,
        help=(
            "Adds a `researcher` subagent with a Pydantic response_format. "
            "Provider-dependent: the Groq models here reject it, because a subagent "
            "always carries filesystem tools."
        ),
    )
    use_code_interpreter = st.sidebar.toggle(
        "Code interpreter (QuickJS)", value=False, help="Adds a sandboxed eval tool."
    )

    with st.sidebar.expander("System prompt"):
        system_prompt = st.text_area("Input context", value=DEFAULT_SYSTEM_PROMPT, height=140)

    st.sidebar.subheader("Thread")
    st.sidebar.caption(f"`{st.session_state.thread_id[:8]}…`")
    st.sidebar.button("🔄 New thread", use_container_width=True, on_click=new_thread)
    st.sidebar.caption(
        "A checkpointer scopes conversation memory to the thread. "
        "StoreBackend files survive a new thread; StateBackend files do not."
    )

    return AgentConfig(
        model=model,
        backend=backend,
        system_prompt=system_prompt,
        use_web_search=use_web_search,
        use_skills=use_skills,
        use_memory=use_memory,
        use_subagents=use_subagents,
        use_planning=use_planning,
        use_structured_subagent=use_structured_subagent,
        use_code_interpreter=use_code_interpreter,
    )


# --------------------------------------------------------------------------- #
# Tabs
# --------------------------------------------------------------------------- #
def chat_tab(built: BuiltAgent, config: dict) -> None:
    for turn in st.session_state.history:
        with st.chat_message(turn["role"]):
            if turn["role"] == "user":
                st.markdown(turn["content"])
            else:
                render_turn(turn)

    prompt = st.chat_input("Ask the deep agent to research, plan, or write files…")
    if not prompt:
        return

    st.session_state.history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Planning and working…"):
            turn = stream_turn(built, prompt, config)
        render_turn(turn)

    st.session_state.history.append({"role": "assistant", **turn})
    if turn.get("todos"):
        st.session_state.last_todos = turn["todos"]

    # Cache the post-run state so the Plan/Files tabs show fresh data.
    try:
        st.session_state.last_state = built.agent.get_state(config).values
    except Exception:
        st.session_state.last_state = None
    st.rerun()


def plan_tab(state_values: dict | None) -> None:
    # Streamed plan first: the main graph's state has no `todos` when the work
    # happened inside a subagent, which has its own middleware stack.
    todos = st.session_state.get("last_todos") or (state_values or {}).get("todos") or []
    if not todos:
        st.info(
            "No plan recorded yet. The agent only calls `write_todos` when it judges "
            "a request complex enough (roughly three or more steps) — and if it "
            "delegates the whole job to a subagent, that subagent's planning is not "
            "visible here. Check **Planning (todo list)** is on in the sidebar."
        )
        return
    st.caption("The agent's own task list, from its planning tool.")
    for todo in todos:
        status = todo.get("status", "pending")
        st.markdown(f"{TODO_ICONS.get(status, '⬜')} {todo.get('content', '')}")


def files_tab(built: BuiltAgent, state_values: dict | None) -> None:
    st.caption(f"Backend: **{built.config.backend}** — {BACKEND_HELP[built.config.backend]}")
    files = list_backend_files(built, state_values)
    if not files:
        st.info("No files yet. Ask the agent to write one, e.g. *create /notes/todo.txt*.")
        return
    for path, content in sorted(files.items()):
        with st.expander(f"📄 {path}  ·  {len(content)} chars"):
            st.code(content[:8000] + ("\n… truncated" if len(content) > 8000 else ""))


def features_tab() -> None:
    st.markdown(
        """
### What this app exercises

| Feature | Where it came from | How to see it |
| --- | --- | --- |
| **Planning / todos** | `1-basicdeepagent` | Ask for multi-step work, watch the **Plan** tab |
| **Virtual filesystem** | `1-basicdeepagent`, `3-backends` | *"Create /notes/todo.txt …"*, then the **Files** tab |
| **Web search tool** | `1-basicdeepagent` | Ask something current; expand the 🔧 `web_search` call |
| **Subagents** (+ per-subagent model) | `2-contextengineering`, `subagents` | *"Research A and B in parallel, then write a report"* |
| **Structured output subagent** | `subagents` | Sidebar toggle (provider-dependent — see below) |
| **System prompt as input context** | `2-contextengineering` | Edit it in the sidebar |
| **AGENTS.md memory** | `2-contextengineering` | *"What's in your memory? Who are you?"* |
| **Skills** | `2-contextengineering` | *"What skills do you have, and when would you use each?"* |
| **Code interpreter** | `2-contextengineering` | Toggle it on, then ask for a computation |
| **Thread memory (checkpointer)** | `2-contextengineering` | Refer back to earlier turns; **New thread** forgets |

### Backends — same agent code, different durability

| Backend | Lives in | Cross-thread? | Survives restart? | Real file on disk? |
| --- | --- | --- | --- | --- |
| `StateBackend` | LangGraph state | No | No | No |
| `FilesystemBackend` | Your disk (`root_dir`) | Yes | Yes | Yes |
| `StoreBackend` | A LangGraph store | Yes | Only with a persistent store | No |

**Try the cross-thread proof:** on `StoreBackend`, ask the agent to write
`/notes/todo.txt`, hit **New thread**, then ask it to read the file back — it can.
Repeat on `StateBackend` and it cannot.

### One caveat on structured-output subagents

`subagents.ipynb` gives a subagent a Pydantic `response_format`. That is off by
default here because it does not work on the Groq models available to this
project: deepagents always hands a subagent filesystem tools, Groq refuses native
JSON mode alongside tool calling, and `ToolStrategy`'s forced `tool_choice` is not
honoured by the `gpt-oss` / `qwen` models. Toggle it on with a provider that
permits both.
"""
    )


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #
def main() -> None:
    init_state()
    cfg = sidebar()
    built = get_agent(cfg)
    config = {"configurable": {"thread_id": st.session_state.thread_id}}

    st.title("Deep Agent Chat")
    st.caption(
        f"{cfg.model} · {cfg.backend} · "
        f"{'subagents' if cfg.use_subagents else 'no subagents'} · "
        f"{'skills' if cfg.use_skills else 'no skills'}"
    )
    for note in built.notes:
        st.warning(note, icon="⚠️")

    state_values = st.session_state.last_state
    chat, plan, files, features = st.tabs(["💬 Chat", "✅ Plan", "📁 Files", "ℹ️ Features"])
    with chat:
        chat_tab(built, config)
    with plan:
        plan_tab(state_values)
    with files:
        files_tab(built, state_values)
    with features:
        features_tab()


if __name__ == "__main__":
    main()
