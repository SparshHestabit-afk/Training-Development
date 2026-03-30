# using class for better encapsulation, as it helps with state management, keeping(state+behavior)
# 
class SessionMemory:

    def __init__(self, max_history=10):
        self.history = [] # storing conversation (chat history)
        self.max_history = max_history # it is used for context window, to limit the number of messages being kept
        # doing it for token control, as llm have only fix number of tokens

    # ADD MESSAGE
    def add(self, role, content):
        if not content:
            return

        self.history.append({
            "role": role,
            "content": str(content).strip()
        })

        # Keeping last N interactions, implemeting a context window, where only N last messages are kept,
        # rest flows out of window, maintaining the window size
        if len(self.history) > self.max_history:
            self.history.pop(0)

    # GET CONTEXT
    def get_context(self):
        if not self.history:
            return ""

        # formatting the context,for clear visualization or representation, using it for making the context LLM-READY
        return "\n".join([
            f"{item['role'].upper()}: {item['content']}"
            for item in self.history
        ])
    
    # UPDATING CONTEXT
    # this is used to update the context, based on the relevance, for the final system prompt
    def update_context(self, messages):
        context = self.get_context() # retrieves the last or previous chat

        if not context:
            return messages

        # this wrappes the retrieved chat into a structured message, with stating this is a previous chat , nothing new
        memory_message = {
            "role": "system",
            "content": f"Recent Conversation:\n{context}"
        }
        # this is the "LIST SANDWITCH", where it retrievaes all the message in the chat history except for the last one, then
        # place the memory exactly in the middle, and then places the latest user prompt or query at the very end

        # we do this, because LLM prioritize the last message they read, and doing this will ensure, LLM goes through the 
        # memory once, before generating any new response, ensuring memory recall, in case the chat or response (for the prompt), exist
        return messages[:-1] + [memory_message] + [messages[-1]]

    # CLEAR MEMORY (to clean everything in memory, and start a fresh session)
    def clear(self):
        self.history = []

    # MEMORY SIZE (for statistics, returning the number of stored messages in memory)
    def size(self):
        return len(self.history)