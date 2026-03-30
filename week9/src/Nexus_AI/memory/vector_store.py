import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class VectorStore:

    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.dimension = 384
        self.index = faiss.IndexFlatL2(self.dimension)
        self.texts = []

    # ADD TEXT
    def add(self, text):
        if not text or len(str(text).strip()) == 0:
            return

        text = str(text).strip()
        embedding = self.model.encode([text])
        embedding = np.array(embedding).astype("float32")

        # Normalize for better similarity
        faiss.normalize_L2(embedding)
        self.index.add(embedding)
        self.texts.append(text)

    # SIMILAR SEARCH
    def search(self, query, k=3):
        if len(self.texts) == 0:
            return []

        query_vec = self.model.encode([query])
        query_vec = np.array(query_vec).astype("float32")
        faiss.normalize_L2(query_vec)
        
        k = min(k, len(self.texts))
        distances, indices = self.index.search(query_vec, k)

        results = []
        for idx in indices[0]:
            if 0 <= idx < len(self.texts):
                results.append(self.texts[idx])
        return results
    
    # UPDATING CONTEXT
    def update_context(self, messages, query, k=3):
        results = self.search(query, k=k)
        
        if not results:
            return messages
        memory_message = {
            "role": "system",
            "content": "Relevant Past Information:\n" + "\n".join(results) # combining the found matches into a single response, to make it LLM understandable
        }
        
        return messages[:-1] + [memory_message] + [messages[-1]]

    # STORE SIZE
    def size(self):
        return self.index.ntotal
    
    # CLEAR MEMORY
    def clear(self):
        self.index.reset()
        self.texts = []