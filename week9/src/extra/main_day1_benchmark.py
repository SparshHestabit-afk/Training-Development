import asyncio
import os
import time

from dotenv import load_dotenv

from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import MaxMessageTermination
from autogen_agentchat.base import TaskResult 
from autogen_agentchat.messages import TextMessage

# Import our modular agents
from agents.research_agent import get_research_agent
from agents.summary_agent import get_summary_agent
from agents.answer_agent import get_answer_agent

async def run_round_robin(model_client, query):
    print("\n" + "="*50)
    print("STRATEGY 1: ROUND ROBIN (FRAMEWORK-LED)")
    print("="*50)
    
    start_time = time.time()
    
    researcher = get_research_agent(model_client)
    summarizer = get_summary_agent(model_client)
    answerer = get_answer_agent(model_client)


    termination = MaxMessageTermination(max_messages=4)
    team = RoundRobinGroupChat(
        participants=[researcher, summarizer, answerer],
        termination_condition=termination
    )

    async for message in team.run_stream(task=query):
        if not isinstance(message, TaskResult):
            source = message.source.upper() if hasattr(message, 'source') else "SYSTEM"
            print(f"\n[{source}]:")
            print(message.content)
            print("-" * 30)

    end_time = time.time()
    return end_time - start_time

async def run_hard_coded(model_client, query):
    print("\n" + "="*50)
    print(" STRATEGY 2: HARD-CODED (MANUAL PIPELINE)")
    print("="*50)
    
    start_time = time.time()

    researcher = get_research_agent(model_client)
    summarizer = get_summary_agent(model_client)
    answerer = get_answer_agent(model_client)

    # FIX: Use TextMessage instead of a dictionary
    user_msg = TextMessage(content=query, source="user")

    # --- STEP 1: RESEARCH ---
    print(f"\n[RESEARCH_AGENT] is thinking...")
    res_task = await researcher.on_messages([user_msg], None)
    res_content = res_task.chat_message.content
    print(f"DONE. (Received {len(res_content)} characters)")

    # --- STEP 2: SUMMARIZE ---
    print(f"\n[SUMMARIZER_AGENT] is processing...")
    # Wrap the researcher's output in a TextMessage for the summarizer
    res_msg = TextMessage(content=res_content, source="researcher")
    sum_task = await summarizer.on_messages([res_msg], None)
    sum_content = sum_task.chat_message.content
    print(f"DONE. (Received {len(sum_content)} characters)")

    # --- STEP 3: FINAL ANSWER ---
    print(f"\n[ANSWER_AGENT] Finalizing Response:\n")
    # Wrap the summary in a TextMessage for the answerer
    sum_msg = TextMessage(content=sum_content, source="summarizer")
    ans_task = await answerer.on_messages([sum_msg], None)
    print(ans_task.chat_message.content)

    end_time = time.time()
    return end_time - start_time

async def main():
    load_dotenv()
    
    model_client = OpenAIChatCompletionClient(
        model=os.getenv("LLM_MODEL"), 
        api_key=os.getenv("LLM_API_KEY"), 
        base_url=os.getenv("LLM_BASE_URL"),
        model_info={
            "vision": False,
            "function_calling": True,
            "json_output": True,
            "family": "unknown",
            "structured_output": True,
        }
    )

    print("\n--- AGENT BENCHMARK TERMINAL ---")
    query = input("Enter research topic for benchmarking: ")
    
    if not query.strip():
        query = "What is Machine Learning?"

    # Execute Strategies
    time_rr = await run_round_robin(model_client, query)
    
    print("\n... Cooling down for 2 seconds ...")
    await asyncio.sleep(2)

    time_hc = await run_hard_coded(model_client, query)

    # FINAL REPORT
    print("\n" + "-"*50)
    print("         FINAL PERFORMANCE BENCHMARK")
    print("-"*50)
    print(f"1. Round Robin (Framework): {time_rr:.2f}s")
    print(f"2. Hard-Coded (Manual):    {time_hc:.2f}s")
    print("-" * 50)
    
    winner = "Hard-Coded" if time_hc < time_rr else "Round Robin"
    diff = abs(time_rr - time_hc)
    print(f"WINNER: {winner} (Faster by {diff:.2f}s)")
    print("-"*50 + "\n")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nBenchmark stopped.")