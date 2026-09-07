# LangGraph Skill — Instructions

## Core Concepts
- **StateGraph**: nodes are functions that take the current state and return a partial state update; edges define control flow between nodes; a compiled graph is invoked like a runnable.
- **State schema**: typically a `TypedDict` or Pydantic model describing the fields carried through the graph (messages, todos, files, custom fields). Use `Annotated[list[...], operator.add]` (or LangGraph's reducers) when a field should accumulate rather than overwrite.
- **Conditional edges**: use a router function returning the name of the next node (or `END`) to implement branching logic instead of embedding control flow inside node bodies.
- **Checkpointers**: attach a checkpointer (e.g., `MemorySaver`, a SQLite/Postgres saver) to persist state across invocations and enable resuming a thread.

## Deep Agent Architecture (this repo's convention)
A "deep agent" is not a single ReAct loop — it's a composition of four pieces, all present in `deepagent/1-basicdeepagent.ipynb` and elaborated in later notebooks:

1. **Planning tool** — an explicit todo/plan tool so the agent breaks work into steps and revises the plan as it learns more. Always give the agent a way to write and update this plan rather than relying on ad hoc reasoning in the transcript.
2. **Sub-agents** — delegate bounded, noisy work (research, file exploration) to a sub-agent with its own context window so only the sub-agent's final result re-enters the parent's context. Define sub-agents with a narrow, clearly scoped responsibility.
3. **Virtual filesystem** — use file tools (`ls`, `read_file`, `write_file`, `edit_file`) backed by one of the supported backends (see below) so large intermediate artifacts don't consume the main context window.
4. **Detailed system prompt** — be explicit in the system prompt about when to plan, when to delegate to a sub-agent, when to use the filesystem, and how the agent should signal task completion. Deep agents lean on prompt engineering more than a minimal ReAct agent does.

## Backends
Choose the backend based on the persistence requirement, matching `deepagent/3-backends.ipynb`:
- **In-memory** — state lives only for the run; use for notebooks/demos where persistence isn't needed.
- **Filesystem** — state persists to disk; use when a run should be inspectable or resumable after the process exits.
- **Store-backed (LangGraph `Store`)** — state persists across threads/sessions; use for long-term memory shared across separate conversations.

Don't reach for a store-backed setup by default — only when the task explicitly needs memory beyond a single run.

## Context Engineering
- Offload large tool outputs (search results, file dumps, long API responses) to the virtual filesystem; pass only a summary or file pointer back into the main agent's context.
- Use sub-agent isolation for any exploratory or noisy work — the parent should only see the sub-agent's synthesized report, not its raw tool trace.
- Prefer structured state (todo list, file contents) as the source of truth over relying on the full message history staying coherent over many turns.
- Periodically summarize/compact older conversation history once it's no longer needed verbatim, rather than letting the transcript grow unbounded.

## Skills Middleware Note
This repo's `deepagents` dependency includes a `SkillsMiddleware` that loads skills from directories containing a `SKILL.md` file with YAML frontmatter (`name`, `description`) and exposes them to the agent via progressive disclosure (metadata first, full content read on demand via `read_file`). When building a deep agent here that should use this skills folder, register `deepagent/skills` as a source for that middleware.

## Workflow Before Building/Modifying a Graph
1. Identify whether the task needs a full deep agent (planning + sub-agents + filesystem) or a simpler single-agent graph — don't add deep-agent machinery for a task that's a single tool call.
2. Check existing notebooks for an established pattern before introducing a new state field or node type.
3. Verify LangChain v1 import paths against what's already imported in the notebooks (v1 moved several modules relative to v0.x) rather than assuming v0.x paths still work.
4. After building or editing a graph, run it against a representative input (in the notebook) to confirm nodes execute in the expected order and state updates as intended.
