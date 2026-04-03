import os
import json
import numpy as np
import faiss

from sentence_transformers import SentenceTransformer

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VECTORSTORE_DIR = os.path.join(BASE_DIR, "vectorstore")
CHUNKS_DIR = os.path.join(BASE_DIR, "data", "chunks")
EMBEDDING_DIR = os.path.join(BASE_DIR, "embeddings")

EMBEDDING_PATH = os.path.join(EMBEDDING_DIR, "embedding.npy")
CHUNKS_PATH = os.path.join(CHUNKS_DIR, "chunks.json")
MODEL_NAME = "all-MiniLM-L6-v2"

def create_embeddings():
    print("Loading chunks and metadata....")
    with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    texts = [chunk["text"] for chunk in chunks]

    print(f"Loading embedding model: {MODEL_NAME}")
    model = SentenceTransformer(MODEL_NAME)

    print("Creating embeddings for chunks....")
    embeddings = model.encode(texts, show_progress_bar=True)
    embeddings = np.array(embeddings).astype("float32")

    os.makedirs(EMBEDDING_DIR, exist_ok=True)
    np.save(EMBEDDING_PATH, embeddings)

    print(f"Embeddings created and saved successfully at {EMBEDDING_PATH}")
    print(f"Total Embeddings Created: {embeddings.shape[0]}")

if __name__ == "__main__":
    create_embeddings()