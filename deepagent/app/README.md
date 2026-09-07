# Deep Agent Chat (Streamlit)

A conversational Streamlit chatbot that exercises every deep-agent feature covered in
the notebooks in this folder — planning, the virtual filesystem, subagents, skills,
`AGENTS.md` memory, all three backends, and thread-scoped conversation memory.

## Run it

From the repo root:

```bash
uv run streamlit run deepagent/app/streamlit_app.py
```

Requires these keys in the repo-root `.env` (only the ones you actually select):

| Key | Needed for |
| --- | --- |
| `MISTRAL_API_KEY` | the `mistral-small-latest` model |
| `GROQ_API_KEY` | the `groq:…` models |
| `TAVILY_API_KEY` | the `web_search` tool |

## Layout

- `streamlit_app.py` — the UI: chat, Plan, Files and Features tabs
- `agent_factory.py` — builds the deep agent from the sidebar config, and reads
  files back out of whichever backend is active

## What maps to which notebook

| Feature | Notebook | How to see it in the app |
| --- | --- | --- |
| Model + `web_search` tool + system prompt | `1-basicdeepagent` | Sidebar; expand the 🔧 `web_search` call in a reply |
| Planning / todos (`write_todos`) | `1-basicdeepagent` | Ask for multi-step work → **Plan** tab |
| Virtual filesystem (`result["files"]`) | `1-basicdeepagent`, `3-backends` | *"Create /notes/todo.txt …"* → **Files** tab |
| System prompt as input context | `2-contextengineering` | Sidebar → **System prompt** |
| `AGENTS.md` as durable memory | `2-contextengineering` | *"What's in your memory? Who are you?"* |
| Skills as memory context | `2-contextengineering` | *"What skills do you have, and when would you use each?"* |
| Subagents, incl. per-subagent model | `2-contextengineering`, `subagents` | *"Research A and B in parallel, then write a report"* |
| Structured-output subagent (`response_format`) | `subagents` | Sidebar toggle (off by default — see Notes) |
| Code interpreter (QuickJS) | `2-contextengineering` | Toggle on, then ask for a computation |
| Checkpointer / thread memory | `2-contextengineering` | Refer back to an earlier turn; **New thread** forgets |
| StateBackend / FilesystemBackend / StoreBackend | `3-backends` | Sidebar → **Backend** |

## Seeing the backends differ

The point of `3-backends.ipynb` is that identical agent code behaves differently
depending on where files live. To reproduce that here:

1. Pick **StoreBackend**, ask the agent to create `/notes/todo.txt`.
2. Click **New thread**, then ask it to read `/notes/todo.txt` back. It can —
   store files are shared across threads.
3. Switch to **StateBackend** and repeat. After **New thread** the file is gone,
   because state files live and die with a single thread.

**FilesystemBackend** writes to real disk, rooted at the `deepagent/` folder, so
`skills/` and `projects/AGENTS.md` load straight from disk with nothing to seed —
and anything the agent writes shows up as a real file. `virtual_mode=True` keeps it
confined to that folder.

## Notes

- `StateBackend` and `StoreBackend` have no files of their own, so the app seeds
  `AGENTS.md` and the skill markdown into them (with the first message of a thread
  for state; once per store). `FilesystemBackend` needs no seeding.
- Changing anything in the sidebar rebuilds the agent, which resets the
  checkpointer — so conversation history restarts, by design.
- `TodoListMiddleware` is added explicitly: deepagents 0.7 does not include it by
  default, and it is what provides `write_todos` and the `todos` state channel.
- The **structured-output subagent** from `subagents.ipynb` is off by default. It
  does not work on the Groq models this project can reach: deepagents always gives
  a subagent filesystem tools, Groq rejects native JSON mode combined with tool
  calling (HTTP 400), and `ToolStrategy`'s forced `tool_choice` is not honoured by
  `gpt-oss-120b`, `gpt-oss-20b` or `qwen3.6-27b`. Enable the toggle on a provider
  that allows structured output alongside tools.
- Model list is limited to IDs verified against this project's keys. The
  `groq:qwen/qwen3.6-27b` used in `subagents.ipynb` works;
  `llama-3.3-70b-versatile` and `llama-3.1-8b-instant` return 404 on this account.
