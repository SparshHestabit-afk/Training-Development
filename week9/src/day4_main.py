import os
from groq import Groq
from dotenv import load_dotenv

from memory.session_memory import SessionMemory
from memory.vector_store import VectorStore
from memory.long_term_memory import LongTermMemory

# Setup of LLM , the actual (brain) behind the working
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL_NAME = "llama-3.3-70b-versatile"

# Memory Initialization
session_memory = SessionMemory()
vector_store = VectorStore()
long_memory = LongTermMemory()

# LLM CALL
def call_llm(messages):
    # wrapper function used to interact with AI model via OpenAI-Compatible APIs, 
    # to simplify the process of sending a conversation to the "brain", (LLM MODEL), and getting response back
    response = client.chat.completions.create(
        model=MODEL_NAME, # telling which AI model to use
        messages=messages, # passing the context history, for making LLM understand better
        temperature=0 # for controlling the randomness, this states to be very discrete
    )
    # LLM returns multiple choices, and this ensure to select the first choice, and from that 
    # it extract the final (raw text) response only, rather than complete message structure.
    return response.choices[0].message.content

# EXTRACTING MEANINGFUL MEMORY
# deciding whether the response is to be stored or ignored, based on it's importance
def extract_important_memory(query, response):
    if not response or len(response.split()) < 5:
        return None
    return f"User's Query: {query}\nAssistant's Response: {response}"

# MEMORY STATS
def get_memory_stats():
    return f"""
        MEMORY STATS
        ----------------------
        Session Memory: {session_memory.size()} messages
        Long-Term Memory: {long_memory.count()} records
        Vector Store: {vector_store.size()} embeddings
    """

#  CLEAR MEMORY HANDLER
def handle_clear_command(command):

    if command == "clear session":
        session_memory.clear()
        return " Session memory cleared."

    elif command == "clear long":
        long_memory.clear()
        return " Long-term memory cleared."

    elif command == "clear vector":
        vector_store.clear()
        return " Vector memory cleared."

    elif command == "clear all":
        session_memory.clear()
        long_memory.clear()
        vector_store.clear()
        return " All memory cleared."

    else:
        return "Invalid clear command. Use: clear session / clear long / clear vector / clear all"

# MEMORY PIPELINE
def run(query):

    print("\n[MEMORY SEARCH]")
    # this is a structred base message, used for better LLM understanding
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

    messages = session_memory.update_context(messages) # retrieving context from session memory (gives continuity to conversation)
    messages = vector_store.update_context(messages, query) # retrieving context from vector memory using similarity searching (gives semantic recall)
    messages = long_memory.update_context(messages, query) # retrieving context from long_term memory (gives user personlization)

    print("\n[LLM RESPONSE]")
    response = call_llm(messages) # calling the final LLM for final prompt using the final updated context, where the updated context comprises relevance

    # STORE MEMORY
    print("\n[MEMORY STORED]")
    # storing in the session memory, for maintianing the conversation continuity
    session_memory.add("user", query)
    session_memory.add("assistant", response)

    #stores only the needed or impotant facts in memory, that is semantic memory 
    important_memory = extract_important_memory(query, response)
    if important_memory:
        vector_store.add(important_memory)
        long_memory.add(important_memory)
    return response # final response for the updated and final context prompt   

# CLI
if __name__ == "__main__":

    print("Memory System Ready")

    while True:
        q = input("\n>> ").strip().lower()
        # Exit
        if q == "exit":
            break
        # Stats
        elif q == "stats":
            print(get_memory_stats())
            continue
        # Clear commands
        elif q.startswith("clear"):
            print(handle_clear_command(q))
            continue
        # Normal query
        output = run(q)
        print("\n=== RESPONSE ===")
        print(output)