import os
import json
import tiktoken
from tqdm import tqdm

from src.utils.loader import load_documents

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHUNK_DIR = os.path.join(BASE_DIR, "data", "chunks")

CHUNK_SIZE = 500
CHUNK_OVERLAP = 100
CHUNKS_PATH = os.path.join(CHUNK_DIR, "chunks.json")

encoding = tiktoken.get_encoding("cl100k_base")

def chunk_text(text, metadata):
    tokens = encoding.encode(text)
    chunks = []

    start = 0
    while start < len(tokens):
        end = start + CHUNK_SIZE
        chunk_tokens = tokens[start:end]

        chunks.append({
            "text": encoding.decode(chunk_tokens),
            "metadata": metadata
        })

        start += CHUNK_SIZE - CHUNK_OVERLAP
    
    return chunks

def ingest():
    print("Loading documents....")
    documents = load_documents()
    print(f"Documents Loaded: {len(documents)}")

    all_chunks = []

    for doc in tqdm(documents):
        chunks = chunk_text(doc["text"], doc["metadata"])
        all_chunks.extend(chunks)

    print(f"Total Chunks Created: {len(all_chunks)}")

    os.makedirs(CHUNK_DIR, exist_ok=True)
    with open(CHUNKS_PATH, "w", encoding= "utf-8") as f:
        json.dump(all_chunks, f, ensure_ascii=False, indent=4)

    print("Chunks saved successfully.")

if __name__ == "__main__":
    ingest()