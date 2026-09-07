"""
Streamlit app: Summarize a YouTube video or a website using LangChain +
Hugging Face or Groq.

Run with:
    streamlit run huggingface_langchain/app.py
"""

import os

import streamlit as st
import validators
from dotenv import load_dotenv
from langchain_classic.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import UnstructuredURLLoader, YoutubeLoader
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

st.set_page_config(page_title="URL Summarizer", page_icon="📝")
st.title("📝 Summarize Text From YouTube or a Website")

# ---------------------------------------------------------------------------
# Sidebar: choose a provider and supply its API key
# ---------------------------------------------------------------------------
with st.sidebar:
    st.subheader("Settings")
    provider = st.radio("LLM Provider", ["Hugging Face", "Groq"])

    if provider == "Hugging Face":
        hf_token = st.text_input(
            "Hugging Face API Token",
            value=os.getenv("HUGGINGFACEHUB_API_TOKEN", ""),
            type="password",
            help="Get a free token at https://huggingface.co/settings/tokens",
        )
        groq_api_key = ""
    else:
        groq_api_key = st.text_input(
            "Groq API Key",
            value=os.getenv("GROQ_API_KEY", ""),
            type="password",
            help="Get a free key at https://console.groq.com/keys",
        )
        groq_model = st.text_input("Groq Model", value="openai/gpt-oss-120b")
        hf_token = ""

url = st.text_input("Enter a YouTube or website URL")

PROMPT_TEMPLATE = """
Write a concise summary of the following content in about 300 words:

{text}

CONCISE SUMMARY:
"""
prompt = PromptTemplate(template=PROMPT_TEMPLATE, input_variables=["text"])


def is_youtube_url(u: str) -> bool:
    return "youtube.com" in u or "youtu.be" in u


def load_documents(u: str):
    """Load raw documents from a YouTube or website URL."""
    if is_youtube_url(u):
        loader = YoutubeLoader.from_youtube_url(u, add_video_info=False)
    else:
        loader = UnstructuredURLLoader(
            urls=[u],
            headers={"User-Agent": "Mozilla/5.0"},
        )
    return loader.load()


if st.button("Summarize", type="primary"):
    if provider == "Hugging Face" and not hf_token.strip():
        st.error("Please provide your Hugging Face API token in the sidebar.")
    elif provider == "Groq" and not groq_api_key.strip():
        st.error("Please provide your Groq API key in the sidebar.")
    elif not url.strip():
        st.error("Please enter a URL to summarize.")
    elif not validators.url(url):
        st.error("Please enter a valid URL.")
    else:
        try:
            with st.spinner("Loading content..."):
                documents = load_documents(url)

            if not documents or not "".join(d.page_content for d in documents).strip():
                st.error("No content could be extracted from that URL.")
            else:
                # Split long content into smaller chunks before summarizing.
                splitter = RecursiveCharacterTextSplitter(
                    chunk_size=4000, chunk_overlap=200
                )
                chunks = splitter.split_documents(documents)

                with st.spinner(f"Summarizing with {provider}..."):
                    if provider == "Hugging Face":
                        llm_endpoint = HuggingFaceEndpoint(
                            repo_id="mistralai/Mistral-7B-Instruct-v0.2",
                            provider="featherless-ai",
                            huggingfacehub_api_token=hf_token,
                            temperature=0.5,
                            max_new_tokens=512,
                        )
                        chat_model = ChatHuggingFace(llm=llm_endpoint)
                    else:
                        chat_model = ChatGroq(
                            model=groq_model,
                            api_key=groq_api_key,
                            temperature=0.5,
                        )

                    chain = load_summarize_chain(
                        chat_model,
                        chain_type="map_reduce",
                        map_prompt=prompt,
                        combine_prompt=prompt,
                    )
                    summary = chain.invoke({"input_documents": chunks})["output_text"]

                st.subheader("Summary")
                st.success(summary)

        except Exception as exc:  # noqa: BLE001 - show any failure to the user
            st.error(f"Something went wrong: {exc}")
