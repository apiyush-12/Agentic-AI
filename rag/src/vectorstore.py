from pathlib import Path
import pickle
from typing import List, Any
import faiss
import numpy as np
from src.embedding import EmbeddingPipeline


class FaissVectorStore:
    def __init__(
        self,
        persist_dir=None,
        embedding_model="all-MiniLM-L6-v2",
        chunk_size=1000,
        chunk_overlap=200,
    ):
        rag_dir = Path(__file__).resolve().parent.parent
        self.persist_dir = (
            Path(persist_dir).resolve()
            if persist_dir
            else rag_dir / "faiss_store"
        )
        self.persist_dir.mkdir(
            parents=True,
            exist_ok=True,
        )
        self.faiss_path = (
            self.persist_dir / "faiss.index"
        )
        self.meta_path = (
            self.persist_dir / "metadata.pkl"
        )
        self.index = None
        self.metadata = []

        self.embedding_pipeline = EmbeddingPipeline(
            model_name=embedding_model,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

    def build_from_documents(self, documents):
        if not documents:
            raise ValueError(
                "No documents provided."
            )
        print(
            f"[INFO] Building vector store from "
            f"{len(documents)} documents..."
        )
        chunks = (
            self.embedding_pipeline
            .chunk_documents(documents)
        )
        embeddings = (
            self.embedding_pipeline
            .embed_chunks(chunks)
        )
        metadatas = []
        for chunk in chunks:
            metadata = dict(chunk.metadata)
            metadata["text"] = chunk.page_content
            metadatas.append(metadata)
        
        self.index = None
        self.metadata = []
        self.add_embeddings(
            embeddings,
            metadatas,
        )

        self.save()
        print(
            f"[INFO] Vector store built and saved to "
            f"{self.persist_dir}"
        )

    def add_embeddings(
        self,
        embeddings: np.ndarray,
        metadatas: List[Any] | None = None,
    ):
        if embeddings.ndim != 2:
            raise ValueError(
                "Embeddings must be a 2-dimensional NumPy array."
            )

        dim = embeddings.shape[1]
        if self.index is None:
            self.index = faiss.IndexFlatL2(dim)

        self.index.add(embeddings)
        if metadatas:
            self.metadata.extend(metadatas)
        print(
            f"[INFO] Added {embeddings.shape[0]} "
            f"vectors to FAISS index."
        )

    def save(self):
        if self.index is None:
            raise RuntimeError(
                "Cannot save FAISS index because it has not been built."
            )
        faiss.write_index(
            self.index,
            str(self.faiss_path),
        )
        with open(self.meta_path, "wb") as f:
            pickle.dump(self.metadata, f)
        print(
            f"[INFO] Saved FAISS index: {self.faiss_path}"
        )
        print(
            f"[INFO] Saved metadata: {self.meta_path}"
        )

    def load(self) -> bool:
        if not self.faiss_path.exists():
            print(
                f"[INFO] FAISS index not found: "
                f"{self.faiss_path}"
            )
            return False

        if not self.meta_path.exists():
            print(
                f"[INFO] FAISS metadata not found: "
                f"{self.meta_path}"
            )
            return False

        self.index = faiss.read_index(
            str(self.faiss_path)
        )

        with open(self.meta_path, "rb") as f:
            self.metadata = pickle.load(f)

        print(
            f"[INFO] Loaded FAISS index from "
            f"{self.faiss_path}"
        )

        print(
            f"[INFO] Index contains "
            f"{self.index.ntotal} vectors."
        )

        return True

    def search(
        self,
        query_embedding: np.ndarray,
        top_k: int = 5,
    ):
        if self.index is None:
            raise RuntimeError(
                "FAISS index is not loaded or built."
            )
        if self.index.ntotal == 0:
            return []

        # Prevent requesting more results than exist
        top_k = min(top_k, self.index.ntotal)
        D, I = self.index.search(
            query_embedding,
            top_k,
        )
        results = []
        for idx, dist in zip(I[0], D[0]):
            # FAISS may return -1 when no neighbor exists
            if idx == -1:
                continue
            meta = (
                self.metadata[idx]
                if idx < len(self.metadata)
                else None
            )
            results.append(
                {
                    "index": int(idx),
                    "distance": float(dist),
                    "metadata": meta,
                }
            )
        return results

    def query(
        self,
        query_text: str,
        top_k: int = 5,
    ):
        if self.index is None:
            raise RuntimeError(
                "FAISS index is not loaded or built."
            )
        print(
            f"[INFO] Querying vector store for: "
            f"'{query_text}'"
        )
        query_emb = (
            self.embedding_pipeline
            .embed_query(query_text)
        )
        return self.search(
            query_emb,
            top_k=top_k,
        )


if __name__ == "__main__":
    from src.data_loader import load_all_documents
    docs = load_all_documents()
    store = FaissVectorStore()
    if not store.load():
        store.build_from_documents(docs)
    results = store.query(
        "What is attention mechanism?",
        top_k=3,
    )
    for result in results:
        print(result)