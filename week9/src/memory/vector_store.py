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

        # Normalize (improves similarity search)
        faiss.normalize_L2(embedding)
        self.index.add(embedding)
        self.texts.append(text)

    # SEARCH SIMILAR
    def search(self, query, k=3): # where k defines number of max response we can have, meaning giving the top 3 from many responses
        if len(self.texts) == 0:
            return []

        # creating query embedding (to perform the simialrity searching)
        query = str(query).strip()
        query_vec = self.model.encode([query])
        query_vec = np.array(query_vec).astype("float32")

        # Normalizing query vector for effcienct similarity searching, using stadard scaler
        faiss.normalize_L2(query_vec)

        # Prevent crash if k > available data
        k = min(k, len(self.texts)) # ensures working, in case number of responses are less than k 
        distances, indices = self.index.search(query_vec, k) #similarity search execution for very embedding with query vector

        results = []
        for idx in indices[0]:
            if 0 <= idx < len(self.texts):
                results.append(self.texts[idx]) # adds the response found on search to the list, where text instead of ID/Vector is stored

        return results # list of the final result found based on similarity search
    
    # UPDATING CONTEXT
    def update_context(self, messages, query, k=3):
        results = self.search(query, k=k)
        if not results:
            return messages
        memory_message = {
            "role": "system",
            "content": "Relevant Past Information:\n" + "\n".join(results) # combining the found matches into a single response, to make it LLM understandable
        }
        return messages[:-1] + [memory_message] + [messages[-1]] # return the list with all the history execept for the last one, then memory, and then the user query or prompt

    # STORE SIZE
    def size(self):
        return self.index.ntotal

    # CLEAR MEMORY
    def clear(self):
        self.index.reset()
        self.texts = []