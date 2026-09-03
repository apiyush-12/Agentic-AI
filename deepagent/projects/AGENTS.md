# Agents.md — Deep Agent Context

This file is meant to be loaded as context whenever a deep agent is invoked
in this project. It summarizes the architecture, components, and conventions
used across the notebooks in `deepagent/` so an agent has a consistent mental
model before it starts planning or executing tasks.

## What is a Deep Agent

A "deep agent" (as implemented via LangChain's `deepagents` / `langgraph`
building blocks) is an agent architecture designed for long-horizon,
multi-step tasks — as opposed to a single-shot ReAct loop. It combines four
core pieces:

1. **Planning tool** — an explicit todo/plan tool the agent uses to break a
   task into steps, track progress, and revise the plan as it learns more.
   This keeps the agent goal-directed over many tool calls instead of
   drifting.
2. **Sub-agents** — the main agent can delegate a bounded piece of work to a
   sub-agent with its own context window. This isolates noisy tool output
   (search results, file dumps) from the main agent's context, and lets
   sub-agents specialize (e.g., a "research" sub-agent vs. a "critique"
   sub-agent).
3. **Virtual filesystem / file tools** — a scratch filesystem (in-memory or
   backed by a real store) the agent uses to write intermediate artifacts
   (notes, drafts, extracted data) instead of carrying everything in the
   context window. Tools typically include `ls`, `read_file`, `write_file`,
   `edit_file`.
4. **A detailed system prompt** — deep agents rely heavily on prompt
   engineering to describe when to plan, when to delegate, when to use the
   filesystem, and how to signal task completion.

## Backends

The agent's state (filesystem, todos, long-term memory) can be backed by
different storage layers, swappable without changing agent logic:

- **In-memory backend** — state lives only for the duration of a single run;
  fastest, no persistence. Good for notebooks/demos.
- **Filesystem backend** — state is persisted to disk, so a run can be
  resumed or inspected after the fact.
- **Store-backed (e.g., LangGraph `Store`)** — state persists across threads
  and runs, enabling long-term memory shared across sessions.

See `deepagent/3-backends.ipynb` for concrete backend configuration examples.

## Context Engineering

Because deep agents run for many steps, the biggest failure mode is context
window overflow or dilution (too much irrelevant tool output crowding out
the actual task). Key techniques used in this project:

- **Offload to files** — write large tool outputs to the virtual filesystem
  and pass only a summary/pointer back into the main context.
- **Sub-agent isolation** — run noisy, exploratory work in a sub-agent so
  only its final report re-enters the parent's context.
- **Summarization/compaction** — periodically compress older conversation
  history once it's no longer needed verbatim.
- **Structured state over raw transcript** — prefer explicit todo lists and
  file contents as the source of truth over relying on the full message
  history.

See `deepagent/2-contextengineering.ipynb` for worked examples.

## Conventions for This Repo

- Notebooks are numbered in the order they should be read/run
  (`1-basicdeepagent.ipynb`, `2-contextengineering.ipynb`,
  `3-backends.ipynb`, ...).
- LLM provider API keys are loaded from `.env` via `python-dotenv`; do not
  hardcode keys in notebooks.
- This project targets LangChain v1.x APIs — check notebook imports for the
  exact module paths in use, since v1 reorganized several packages relative
  to v0.x.

## When Invoked as a Deep Agent Here

- Prefer writing intermediate research/drafts to files under
  `deepagent/projects/` (or a scratch subfolder) rather than inlining large
  content into the conversation.
- Use the planning tool to lay out multi-step notebook edits before making
  them, especially when a task spans multiple notebooks.
- Delegate exploratory search/research to sub-agents; keep the main agent's
  context focused on decisions and final edits.
