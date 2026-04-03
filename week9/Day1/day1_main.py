# as LLM calls are io-bound, it allows the use of await, so that multiple agents can operate concurrently, important for message passing as well.
import asyncio
import os
# provides access to system-specific parameters and functions, allowing code to interact with the Python interpreter and its runtime environment
import sys
# used for time.perf_counter() , which is a high resolution timer to calculate the performance time
import time

# used to load env configuration to our file, by fetching it from there , without risk of exposure
from dotenv import load_dotenv

# autogen uses this library or extension to wrap our local ollama api to look like OpenAi, compatible endpoint, 
# because OPENAI became the gold standard for API, so ollama is wraped to make it upto standard, or adapting to standard, 
# as well as AutoGen speaks OPENAI standard
from autogen_ext.models.openai import OpenAIChatCompletionClient

# autogen uses this library to wrap raw text into this object, as it is a structured data type, 
# with the purpose of allowing to track source(who said it [which agent in our case]) and metadata about the text or response.
from autogen_agentchat.messages import TextMessage

# Importing or defined agents
from agents.research_agent import get_research_agent
from agents.summary_agent import get_summary_agent
from agents.answer_agent import get_answer_agent

# we are using asynchronous execution for concurreny, and efficient multi-agent collaboration and message passing
async def main():
    # loading our LLM configuration file (.env), 
    # where we use getenv to fetch the value of a variable from our .env file
    load_dotenv()
    
    # 1. Model Client Configuration
    model_client = OpenAIChatCompletionClient(
        model=os.getenv("LLM_MODEL"), 
        api_key="ollama", 
        base_url=os.getenv("LLM_BASE_URL"),
        # it js the information about the capabilities, features and constraints model provide, specifying what task it can perform
        model_info={
            "vision": False,  # declares model cannot process images
            "function_calling": False, # declares model cannot perform tool/function calling (everything stays text based reasoning)
            "json_output": False, # declares model cannot reliably produce JSON outputs, (responses treated as plain text)
            "structured_output": False, # declared model cannot generate schema-based outputs, meaning no guaranteed structured responses
            "family": "unknown" # declares model type is unspecified, where it generaly optimize it's behavior for known model family
        }
    )

    # 2. Initialize Agents, parsing openai client wrapper to our agents, for parsing agent responses to be in OpenAi standard, and allowing communication with other models as well
    researcher = get_research_agent(model_client)
    summarizer = get_summary_agent(model_client)
    answerer = get_answer_agent(model_client)

    print("\n" + "="*50)
    print("MULTI-AGENT RESEARCH TERMINAL (DAY 1)")
    print("Type 'quit' or 'exit' to end the session.")
    print("="*50)

    while True:
        # --- EMPTY QUERY HANDLING ---
        raw_input = input("\n Enter Research Topic: ")
        query = raw_input.strip()
        
        if not query:
            print("Error: Query cannot be empty. Please enter a topic.")
            continue
            
        if query.lower() in ["quit", "exit"]:
            print("\nShutting down agents... Goodbye!")
            break

        start_total = time.perf_counter()

        try:
            # --- STAGE 1: RESEARCH ---
            print(f"\n[*] Running {researcher.name}...")
            s1 = time.perf_counter()

            # in this method we pass a list of messages to the agent and waits for full, final answer/response
            # this method tells the agent: "Take this input, think completely, and give me the final result as one single block of text."
            res_task = await researcher.on_messages([TextMessage(content=query, source="user")], None)
            # in this line , res_task, provides us the result object, ehich actually is a structured message, which have source, metadata, and extra info, along with response text
            # chat_message filters out that extra segment(metadata, timing, ids, etc), and content give us the raw text  or final context(content/response), we want
            research_buffer = res_task.chat_message.content
            e1 = time.perf_counter()
            # it is used to clean the empty spaces, in case LLM return one, where if LLM failes, it breaks the pipeline,
            # where research_buffer is the temporary storage , containing the response from the researcher_agent
            if not research_buffer.strip(): 
                print(" Research query fails."); continue # HERE ; is the python statement separator, used for small but related statement to be put together in a line, so that we can understand better and does not loose the relevance 
            
            print(f"\n--- {researcher.name.upper()} OUTPUT ---\n{research_buffer}\n")
            print(f"Time: {e1 - s1:.2f}s")

            # --- STAGE 2: SUMwMARY ---
            print(f"\n[*] Running {summarizer.name}...")
            s2 = time.perf_counter()
            sum_task = await summarizer.on_messages([TextMessage(content=research_buffer, source="researcher")], None)
            summary_buffer = sum_task.chat_message.content
            e2 = time.perf_counter()
            
            if not summary_buffer.strip(): 
                print("Summarization query fails."); continue

            print(f"\n--- {summarizer.name.upper()} OUTPUT ---\n{summary_buffer}\n")
            print(f"Time: {e2 - s2:.2f}s")

            # --- STAGE 3: FINAL ANSWER ---
            print(f"\n[*] Running {answerer.name}...")
            s3 = time.perf_counter()
            ans_task = await answerer.on_messages([TextMessage(content=summary_buffer, source="summarizer")], None)
            final_answer = ans_task.chat_message.content
            e3 = time.perf_counter()
            
            if not final_answer.strip(): 
                print("Final Answer query fails."); continue
            print(f"Time: {e3 - s3:.2f}s")

            # --- FINAL OUTPUT ---
            print("\n" + "-"*30 + " FINAL RESPONSE " + "-"*30)
            print(final_answer)
            print("-"*76)

            end_total = time.perf_counter()
            print(f"\nTOTAL PIPELINE TIME: {end_total - start_total:.2f}s")

        except Exception as e:
            print(f"\nCRITICAL ERROR: {e}")
            break
    
    # closing or shutting down model client after using it, because model client (OPENAICHATCOMPLETIONCLIENT) internally manages various tasks
    # like network connections, async resources and etc. which aren't closed automatically, and not doing so can result in memory leakage, too many
    # open connection and Warnings like (unclosed client session), also performace degradation over time
    await model_client.close()

if __name__ == "__main__":
    try:
        asyncio.run(main()) # running or main execution in asnychronous mode for non-blocking execution
    except KeyboardInterrupt:
        sys.exit(0)