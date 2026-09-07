# URL Summarizer (Streamlit + LangChain)

A small Streamlit app that summarizes the content of a **YouTube video** or a
**website** using LangChain, with your choice of **Hugging Face** (via the
`featherless-ai` provider) or **Groq** as the LLM backend.

## Features

- Accepts a YouTube or website URL and validates it with `validators`
- Auto-detects YouTube vs. website links and loads content with
  `YoutubeLoader` or `UnstructuredURLLoader`
- Splits long content into chunks with `RecursiveCharacterTextSplitter`
  before summarizing
- Summarizes with LangChain's `load_summarize_chain` (`map_reduce`)
- Switch between **Hugging Face** and **Groq** from the sidebar
- Friendly error messages for missing tokens, invalid URLs, or failed loads

## Setup

From the repo root, with the project's `uv`-managed virtual environment:

```bash
uv sync
```

Or with plain `pip`:

```bash
pip install streamlit langchain-community langchain-huggingface \
    langchain-groq langchain-text-splitters langchain-classic \
    langchain-core python-dotenv unstructured youtube-transcript-api validators
```

### API keys

You need an API key for **at least one** provider:

- **Hugging Face**: free token at https://huggingface.co/settings/tokens
- **Groq**: free key at https://console.groq.com/keys

Either paste the key directly into the app's sidebar at runtime, or set it in
a `.env` file at the repo root so it's prefilled automatically:

```
HUGGINGFACEHUB_API_TOKEN=hf_xxxxxxxxxxxxxxxxxxxx
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxx
```

## Running the app

From the repo root (`A:\langchainupdated`):

```powershell
A:\langchainupdated\.venv\Scripts\python.exe -m streamlit run huggingface_langchain\app.py
```

Or activate the venv first:

```powershell
& "A:\langchainupdated\.venv\Scripts\Activate.ps1"
streamlit run huggingface_langchain\app.py
```

Streamlit will print a local URL (default `http://localhost:8501`) — open it
in your browser.

> **Note:** run this command from the repo root, using the path
> `huggingface_langchain\app.py` relative to it. If you `cd` into the
> `huggingface_langchain` folder first, use `app.py` instead — do not repeat
> `huggingface_langchain\huggingface_langchain\app.py`, that path only exists
> if the folder was accidentally nested.

## Usage

1. Pick a provider (**Hugging Face** or **Groq**) in the sidebar.
2. Enter the matching API key (or rely on the `.env` values).
3. Paste a YouTube or website URL in the main input box.
4. Click **Summarize** and wait for the result.

## How it works

| Step | Component |
|---|---|
| URL validation | `validators.url()` |
| YouTube vs. website detection | substring check on `youtube.com` / `youtu.be` |
| Content extraction | `YoutubeLoader` or `UnstructuredURLLoader` |
| Chunking | `RecursiveCharacterTextSplitter` (4000 chars, 200 overlap) |
| Summarization | `load_summarize_chain` (`map_reduce`) with a custom `PromptTemplate` |
| LLM | `ChatHuggingFace` + `HuggingFaceEndpoint` (`provider="featherless-ai"`) or `ChatGroq` |
