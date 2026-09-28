from typing import List, Any
import numpy as np
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer


class EmbeddingPipeline:
    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2",
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ):
        self.model_name = model_name
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.model = SentenceTransformer(model_name)
        print(f"[INFO] Loaded embedding model: {model_name}")

    def chunk_documents(self, documents: List[Any]) -> List[Any]:
        if not documents:
            return []
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""],
        )
        chunks = splitter.split_documents(documents)
        print(
            f"[INFO] Split {len(documents)} documents "
            f"into {len(chunks)} chunks."
        )
        return chunks

    def embed_chunks(self, chunks: List[Any]) -> np.ndarray:
        if not chunks:
            return np.empty((0, 0), dtype=np.float32)
        texts = [
            chunk.page_content
            for chunk in chunks
        ]
        print(
            f"[INFO] Generating embeddings "
            f"for {len(texts)} chunks..."
        )
        embeddings = self.model.encode(
            texts,
            show_progress_bar=True,
            convert_to_numpy=True,
        )
        embeddings = embeddings.astype("float32")
        print(
            f"[INFO] Embeddings shape: "
            f"{embeddings.shape}"
        )
        return embeddings

    def embed_query(self, query: str) -> np.ndarray:
        embedding = self.model.encode(
            [query],
            convert_to_numpy=True,
        )
        return embedding.astype("float32")


if __name__ == "__main__":
    from src.data_loader import load_all_documents
    docs = load_all_documents()
    emb_pipe = EmbeddingPipeline()
    chunks = emb_pipe.chunk_documents(docs)
    embeddings = emb_pipe.embed_chunks(chunks)
    if len(embeddings) > 0:
        print(
            "[INFO] Example embedding shape:",
            embeddings[0].shape,
        )