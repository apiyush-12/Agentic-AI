from src.data_loader import load_all_documents
from src.vectorstore import FaissVectorStore


documents = load_all_documents()
store = FaissVectorStore()

if not store.load():
    raise RuntimeError("FAISS index not found. Build the vector store first.")

print("[INFO] FAISS vector store loaded successfully.")

while True:
    query = input("\nAsk a question (type 'exit' to quit): ")
    if query.lower() in ["exit", "quit"]:
        break
    results = store.query(query, top_k=3)
    print("\nTop matching chunks:\n")

    for i, result in enumerate(results, start=1):
        metadata = result["metadata"]
        print(f"\nResult {i}")
        print(f"Distance: {result['distance']}")
        if metadata:
            print(metadata.get("text", ""))
        print("-" * 80)

