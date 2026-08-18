# Plan: Vectorless RAG Notebook with PageIndex

## Context

This repo (`A:\langchainupdated`) is a LangChain v1.3.14 learning collection of numbered Jupyter notebooks (`1-langchainintro.ipynb` … `5-structuredoutput.ipynb`) each teaching one concept (agents, model integration, tools, messages, structured output) using multiple LLM providers via `init_chat_model()`.

The user wants a new notebook demonstrating **vectorless RAG** using the **PageIndex** library — an alternative to embedding-based RAG that builds a hierarchical tree index over a document's structure (like a table of contents) and uses an LLM to *reason* over that tree to find the relevant section, instead of chunking + embedding + vector similarity search. The goal is a self-contained teaching notebook consistent with the rest of the repo's style.

No PageIndex package, PDF-handling library, or sample document currently exist in the repo — all need to be added.

## Approach

Use the **PageIndex OSS Python package** (not the hosted Cloud API) as the primary path, since it's fully self-contained and reuses the `OPENAI_API_KEY` already present in `.env` — no new account/API key needed. Briefly mention the Cloud API as an aside (markdown only, no code).`

Sample document: download **"Attention Is All You Need"** (arXiv:1706.03762) at runtime — short, freely available, and has a clean hierarchical section structure (Abstract → Introduction → Background → Model Architecture → 3.1–3.5 subsections → Training → Results → Conclusion) that's ideal for demonstrating tree-based node selection.

## Files to create/modify

- **New:** `updatedlangchain/6-vectorlessrag.ipynb`
- **New:** `.gitignore` (repo root currently has none) — cover `.env`, `.venv/`, `__pycache__/`, `.ipynb_checkpoints/`, and `updatedlangchain/data/*.pdf` (PDF is runtime-downloaded, not committed)
- **Modify:** `pyproject.toml` — add `pageindex`, `pypdf` to `dependencies`
- **Modify:** `requirements.txt` — add `pageindex`, `pypdf`
- No `.env` changes needed — reuses existing `OPENAI_API_KEY`

## Notebook cell-by-cell plan

1. **Markdown** — Title `### Vectorless RAG (PageIndex)`. Contrast traditional vector RAG (chunk → embed → similarity search → stuff top-k chunks) vs. vectorless/reasoning-based RAG (build a tree mirroring doc structure → LLM reasons over titles/summaries like flipping through an index → retrieve the exact section). Note trade-off: no embeddings/vector DB, but requires structured documents and extra LLM calls at index-build time.

2. **Markdown** — `### Setup`. One-liner on installing `pageindex`/`pypdf` and reusing `OPENAI_API_KEY`.

3. **Code** — imports + env:
   ```python
   import os
   from dotenv import load_dotenv
   load_dotenv()
   os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
   ```
   (follows notebook 1's self-contained `load_dotenv()` convention rather than notebook 3/5's implicit assumption)

4. **Markdown** — `### Sample document`. Explain why the transformer paper's clear ToC is a good demo fit.

5. **Code** — download PDF into `updatedlangchain/data/attention_is_all_you_need.pdf`:
   ```python
   import requests
   os.makedirs("data", exist_ok=True)
   PDF_PATH = "data/attention_is_all_you_need.pdf"
   if not os.path.exists(PDF_PATH):
       resp = requests.get("https://arxiv.org/pdf/1706.03762")
       with open(PDF_PATH, "wb") as f:
           f.write(resp.content)
   PDF_PATH
   ```

6. **Markdown** — `### Building the PageIndex tree`. Explain PageIndex uses an LLM to detect section boundaries and build a JSON tree (title, page range, summary per node) — replaces the embedding step.

7. **Code** — build the tree via PageIndex's documented entrypoint (confirm exact function name against installed package at implementation time — see Verification), print the resulting tree object.

8. **Markdown** — `### Inspecting the tree structure`. One sentence: tree mirrors the document's table of contents.

9. **Code** — recursively pretty-print the tree (title, node id, page range, indented by depth) so the hierarchy is visibly readable.

10. **Markdown** — `### Querying: LLM reasoning over the tree`. Explain retrieval is LLM-driven reasoning over node titles/summaries, not embedding similarity.

11. **Code** — run retrieval for a targeted question, e.g. *"How does the paper compute multi-head attention?"* (targets section 3.2.2). Print selected node id(s)/title(s) and any reasoning trace the API returns.

12. **Markdown** — `### Retrieving the section text`. Explain we now pull the full node text (not a chunk) from the source.

13. **Code** — extract the selected node's page range from the PDF via `pypdf.PdfReader` (or a PageIndex helper if available), print a text snippet.

14. **Markdown** — `### Generating the final answer`. Explain returning to LangChain's `init_chat_model()` for answer generation, grounded in the retrieved section.

15. **Code**:
    ```python
    from langchain.chat_models import init_chat_model
    answer_model = init_chat_model("openai:gpt-4o-mini")
    prompt = f"Answer the question using only the context below.\n\nContext:\n{retrieved_text}\n\nQuestion: {question}"
    response = answer_model.invoke(prompt)
    response.content
    ```

16. **Markdown** — `### Comparing to vector-based RAG` (prose only, no code). Describe the equivalent vector RAG pipeline (`PyPDFLoader` → text splitter → embed → vector store → similarity search → stuff into prompt) and trade-offs vs. the vectorless approach just demonstrated.

17. **Markdown** — `### Aside: PageIndex Cloud API`. Brief 2-3 sentence mention of the hosted alternative (submit PDF, call REST endpoints) requiring its own API key — not used here since the OSS path is self-contained.

## Verification

1. **Before writing cells 7/11**, confirm PageIndex's actual API surface: `pip show pageindex`, read its README, and `import pageindex; dir(pageindex)` to get correct function names and check whether it accepts a custom LLM callable (if so, wire in `init_chat_model()` there too instead of relying on direct OpenAI calls).
2. Run the notebook top-to-bottom in Jupyter; confirm no exceptions.
3. Confirm the printed tree (cell 9) resembles the paper's real ToC (Abstract, Introduction, Background, Model Architecture with 3.1–3.5, Results, Conclusion).
4. Ask the cell-11 question (multi-head attention, section 3.2.2) and confirm:
   - Node selection picks section 3.2/3.2.2, not an unrelated section.
   - Retrieved snippet (cell 13) actually contains the multi-head attention description.
   - Final answer (cell 15) is correct and grounded in retrieved context (spot-check it doesn't hallucinate beyond it).
5. Ask a second, different-section question (e.g., optimizer/learning rate schedule, in the Training section) and confirm the tree reasoning selects a *different* node than question 1 — proves discrimination, not a fixed answer.
6. `git status` — confirm `.env` is now excluded, and the new notebook/PDF are tracked/ignored per the `.gitignore` plan.
