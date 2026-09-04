# LangGraph Skill — Examples

## Example 1: Minimal StateGraph with conditional routing

```python
from typing import TypedDict
from langgraph.graph import StateGraph, END


class GraphState(TypedDict):
    question: str
    answer: str
    needs_search: bool


def classify(state: GraphState) -> GraphState:
    needs_search = "latest" in state["question"].lower()
    return {**state, "needs_search": needs_search}


def search_node(state: GraphState) -> GraphState:
    return {**state, "answer": f"searched answer for: {state['question']}"}


def direct_answer(state: GraphState) -> GraphState:
    return {**state, "answer": f"direct answer for: {state['question']}"}


def route(state: GraphState) -> str:
    return "search" if state["needs_search"] else "direct"


builder = StateGraph(GraphState)
builder.add_node("classify", classify)
builder.add_node("search", search_node)
builder.add_node("direct", direct_answer)
builder.set_entry_point("classify")
builder.add_conditional_edges("classify", route, {"search": "search", "direct": "direct"})
builder.add_edge("search", END)
builder.add_edge("direct", END)

graph = builder.compile()
result = graph.invoke({"question": "What are the latest LangGraph features?", "answer": "", "needs_search": False})
```

## Example 2: Basic deep agent (planning + filesystem + sub-agent)

```python
from deepagents import create_deep_agent

agent = create_deep_agent(
    tools=[],  # domain tools go here
    instructions=(
        "You are a research assistant. Use the todo/planning tool to break "
        "multi-step research tasks into steps. Write long intermediate notes "
        "to files instead of keeping them in context. Delegate exploratory "
        "web research to a sub-agent and only bring back its summary."
    ),
    subagents=[
        {
            "name": "researcher",
            "description": "Runs exploratory research and returns a synthesized summary.",
            "prompt": "Research the given topic thoroughly and return a concise, sourced summary.",
        }
    ],
)

result = agent.invoke({"messages": [{"role": "user", "content": "Summarize recent LangGraph releases."}]})
```

## Example 3: Registering the skills folder with SkillsMiddleware

```python
from deepagents.backends.filesystem import FilesystemBackend
from deepagents.middleware.skills import SkillsMiddleware

backend = FilesystemBackend(root_dir="deepagent")
skills_middleware = SkillsMiddleware(
    backend=backend,
    sources=[("/skills", "Deepagent")],
)
```

## Example 4: Filesystem-backed persistence (resume across runs)

```python
from deepagents.backends.filesystem import FilesystemBackend

backend = FilesystemBackend(root_dir="deepagent/projects/scratch")
# Pass `backend` to create_deep_agent(...) so file tool state persists to disk
# between runs instead of vanishing when the process exits.
```

## Example 5: Store-backed long-term memory across threads

```python
from langgraph.store.memory import InMemoryStore
from langgraph.checkpoint.memory import MemorySaver

store = InMemoryStore()       # cross-thread memory
checkpointer = MemorySaver()  # per-thread checkpointing

graph = builder.compile(checkpointer=checkpointer, store=store)
```
