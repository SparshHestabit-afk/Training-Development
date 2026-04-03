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
        embedding = self.model.encode([text]) # converting text into vector embedding
        embedding = np.array(embedding).astype("float32") # turning the embedding into faisss ready format

        # Normalize (improves similarity search)
        faiss.normalize_L2(embedding) # normalizes the vector embedding into a unit vector, as it removes the distance inconsistency
        self.index.add(embedding) # adding the embedding to the faiss index for later similarity searching
        self.texts.append(text) # storing the original text, to make it easy to retrieve the content based on the search result, text mapping 

    # SEARCH SIMILAR
    def search(self, query, k=3): # where k defines number of max response we can have, meaning giving the top 3 from many responses
        if len(self.texts) == 0: # avoids emoty search, when there is no text mapped in the vector store
            return []

        # creating query embedding (to perform the simialrity searching)
        query = str(query).strip() # cleaning query, to retrieve the final text only
        query_vec = self.model.encode([query]) # convert the query into an embedding 
        query_vec = np.array(query_vec).astype("float32") # making the query embedding into faiss ready format

        # Normalizing query vector for effcienct similarity searching, removing distance incosistency
        faiss.normalize_L2(query_vec)

        # Prevent crash if k > available data
        k = min(k, len(self.texts)) # ensures working, in case number of responses are less than k 
        distances, indices = self.index.search(query_vec, k) # similarity search execution for every embedding with query vector

        results = [] # stores the final result, that is the top k similar text from the similarity search
        for idx in indices[0]: # as right now, we have list in list for response, so we take the first list, which is our actual response (faiss support batch queries)
            if 0 <= idx < len(self.texts):
                results.append(self.texts[idx]) # adds the response found on search to the list, where text mapped to that ID/Vector is stored

        return results # list of the final result found based on similarity search
    
    # UPDATING CONTEXT (passing the relevant memory to the llm, based on the query, for the final system prompt, which include memory recall)
    def update_context(self, messages, query, k=3):
        results = self.search(query, k=k) # retrieving the relevant memory
        if not results:
            return messages # in case there is no relevant memory, it return the original message, without modifying the context, or input message
        memory_message = { # creating a strucutred message to make it llm ready
            "role": "system",
            "content": "Relevant Past Information:\n" + "\n".join(results) # combining the found matches into a single response, to make it LLM understandable
        } 
        # this make sure that the memory is once ready by the llm, before generating any new response, ensuring memory recall, in case the similar content exist in the vector store
        return messages[:-1] + [memory_message] + [messages[-1]] # return the list with all the history execept for the last one, then memory, and then the user query or prompt

    # STORE SIZE ( return the final no. of vectors stored, i.e. size of memory)
    def size(self):
        return self.index.ntotal

    # CLEAR MEMORY ( to clean and restart the memory)
    def clear(self):
        self.index.reset()
        self.texts = []