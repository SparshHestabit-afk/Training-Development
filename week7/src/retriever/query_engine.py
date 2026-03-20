import os
import json
import faiss
import numpy as np
import tiktoken

from sentence_transformers import SentenceTransformer

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VECTORSTORE_DIR = os.path.join(BASE_DIR, "vectorstore")

MODEL_NAME = "all-MiniLM-L6-v2"

class QueryEngine:
    def __init__(self):
        print("Loading FAISS and metadata index....")
        self.index = faiss.read_index(os.path.join(VECTORSTORE_DIR, "index.faiss"))

        print("Loading metadata....")
        with open(os.path.join(VECTORSTORE_DIR, "metadata.json"), "r", encoding="utf-8") as f:
            self.metadata = json.load(f)

        print(f"Loading embedding model: {MODEL_NAME}")
        self.model = SentenceTransformer(MODEL_NAME)

    def query(self, query_text, top_k=5):
        query_embedding = self.model.encode([query_text])
        query_embedding = np.array(query_embedding).astype("float32")

        distances, indices = self.index.search(query_embedding, top_k)

        results = []
        for idx in indices[0]:
            if idx < len(self.metadata):
                results.append(self.metadata[idx])

        return results
    
if __name__ == "__main__":
    query_engine = QueryEngine()

    while True:
        query = input("\n Enter your query (or type 'exit' to quit): ")
        if query.lower() == "exit":
            print("Exiting...")
            break

        results = query_engine.query(query)

        print("\n Top Results: \n")
        for i, result in enumerate(results, 1):
            print(f"{i}. {result['metadata']}")
            print(f" {result['text'][:500]} \n")
            print("-" * 50)