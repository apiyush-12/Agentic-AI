---
name: langgraph
description: Design and implement LangGraph graphs, nodes, edges, state schemas, checkpointers, and deep-agent architectures (planning tool, sub-agents, virtual filesystem) used in this repo's deepagent notebooks. Use when the user asks about building agents, graphs, state machines, tool-calling loops, or deep agents with LangChain v1 / LangGraph / deepagents.
metadata:
  type: framework
  framework: langgraph
---

# LangGraph Skill

## When to Use
- The user asks to build, modify, or debug a LangGraph graph (nodes, edges, conditional routing, state schema).
- The user asks about deep agents (`deepagents` package): planning tool, sub-agents, virtual filesystem, backends.
- The user asks about persistence/checkpointing, streaming, or human-in-the-loop patterns in LangGraph.
- The task touches notebooks under `deepagent/` (`1-basicdeepagent.ipynb`, `2-contextengineering.ipynb`, `3-backends.ipynb`).

## How to Use
1. Read `INSTRUCTIONS.md` for the architectural conventions this repo follows for deep agents and LangGraph state/graph design.
2. Read `EXAMPLES.md` for worked code showing graph construction, state schemas, sub-agent delegation, and backend configuration.
3. Match new code to the patterns already established in the `deepagent/` notebooks rather than inventing a new structure.

## Quick Reference
- Core deep agent components: planning tool, sub-agents, virtual filesystem/file tools, detailed system prompt.
- Backends: in-memory (ephemeral), filesystem (persisted to disk), store-backed (cross-thread/session memory via LangGraph `Store`).
- This project targets LangChain v1.x APIs — verify import paths against existing notebook imports since v1 reorganized packages relative to v0.x.
- Prefer offloading large tool outputs to the virtual filesystem instead of inlining them into agent context.
