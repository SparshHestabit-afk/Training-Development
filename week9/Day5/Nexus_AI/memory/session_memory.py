class SessionMemory:

    def __init__(self, max_history=10):
        self.history = []
        self.max_history = max_history

    # ADD MESSAGE
    def add(self, role, content):
        if not content:
            return
        self.history.append({
            "role": role,
            "content": str(content).strip()
        })
        # Keep last N interactions
        if len(self.history) > self.max_history:
            self.history.pop(0)

    # GET CONTEXT
    def get_context(self):
        if not self.history:
            return ""
        return "\n".join([
            f"{item['role'].upper()}: {item['content']}"
            for item in self.history
        ])
    
    # UPDATING CONTEXT
    def update_context(self, messages):
        context = self.get_context() # retrieves the last or previous chat

        if not context:
            return messages
        memory_message = {
            "role": "system",
            "content": f"Recent Conversation:\n{context}"
        }
        return messages[:-1] + [memory_message] + [messages[-1]]

    # MEMORY SIZE
    def size(self):
        return len(self.history)
    
    # CLEAR MEMORY
    def clear(self):
        self.history = []
