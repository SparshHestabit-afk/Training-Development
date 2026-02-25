import os
import json
import numpy as np
import faiss

from sentence_transformers import SentenceTransformer

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHUNK_DIR = os.path.join(BASE_DIR, "data", "chunks")
VECTORSTORE_DIR = os.path.join(BASE_DIR, "vectorstore")

EMBEDDING_PATH = os.path.join(BASE_DIR, "embeddings", "embedding.npy")
CHUNKS_PATH = os.path.join(CHUNK_DIR, "chunks.json")
MODEL_NAME = "all-MiniLM-L6-v2"

def build_index():
    print("Loading embeddings from file....")
    embeddings = np.load(EMBEDDING_PATH)

    print("Loading chunks and metadata....")
    with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    dimensions = embeddings.shape[1]

    print("Building FAISS index....")
    index = faiss.IndexFlatL2(dimensions)
    index.add(embeddings)

    os.makedirs(VECTORSTORE_DIR, exist_ok=True)
    faiss.write_index(index, os.path.join(VECTORSTORE_DIR, "index.faiss"))

    with open(os.path.join(VECTORSTORE_DIR, "metadata.json"), "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=4)

    print("FAISS index and metadata created and saved successfully")
    print(f"Total Vectors Indexed: {embeddings.shape[0]}")

if __name__ == "__main__":
    build_index()