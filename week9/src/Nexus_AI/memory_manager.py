from memory.session_memory import SessionMemory
from memory.vector_store import VectorStore
from memory.long_term_memory import LongTermMemory

class MemoryManager:

    # Initializing various memory stores
    def __init__(self):

        self.session_memory = SessionMemory()
        self.vector_store = VectorStore()
        self.long_memory = LongTermMemory()

    # Retrieving Memory
    def retrieve(self, query):

        print("\n[MEMORY SEARCH]")

        try:
            messages = [
                {
                    "role": "system",
                    "content": "You are a helpful AI assistant with memory. Use context carefully and personalize responses."
                },
                {
                    "role": "user",
                    "content": query
                }
            ]

            messages = self.session_memory.update_context(messages) # retrieving context from session memory (gives continuity to conversation)
            messages = self.vector_store.update_context(messages, query) # retrieving context from vector memory using similarity searching (gives semantic recall)
            messages = self.long_memory.update_context(messages, query) # retrieving context from long_term memory (gives user personlization)

            return messages

        except Exception as e:
            print(f"[MEMORY ERROR] Retrieval Failed: {e}")
            return []
    
    # Storing Memory
    def store(self, query, response):

        print("\n[MEMORY STORE]")

        try:
            # session memory
            self.session_memory.add("user", query)
            self.session_memory.add("assistant", response)

            # Vector memory
            important_memory = f"User asked: {query}\nAssistant answered: {response}"
            self.vector_store.add(important_memory)
            self.long_memory.add(important_memory)

        except Exception as e:
            print(f"[MEMORY ERROR] Storage failed: {e}")

    # Memory Statistics
    def memory_stats(self):
        try:
            return f"""
                MEMORY STATS
                ----------------------
                Session Memory: {self.session_memory.size()} messages
                Long-Term Memory: {self.long_memory.count()} records
                Vector Store: {self.vector_store.size()} embeddings
            """
        except Exception as e:
            return f"Error fetching stats: {e}"
    
    # Memory Cleaner
    def clear(self, command):

        if command == "clear session":
            self.session_memory.clear()
            return "Session memory cleared."
        elif command == "clear long":
            self.long_memory.clear()
            return "Long-term memory cleared."
        elif command == "clear vector":
            self.vector_store.clear()
            return "Vector memory cleared."
        elif command == "clear all":
            self.session_memory.clear()
            self.long_memory.clear()
            self.vector_store.clear()
            return "All memory cleared."
        else:
            return "Invalid clear command."