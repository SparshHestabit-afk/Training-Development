import asyncio
import os
import sys
import time
import re

from dotenv import load_dotenv

from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.messages import TextMessage

# Import agents
from agents.planner_agent import get_planner_agent
from agents.worker_agent import get_worker_agent
from agents.refiner_agent import get_refiner_agent
from agents.validator_agent import get_validator_agent

async def main():
    load_dotenv()
    
    # Client Config
    model_client = OpenAIChatCompletionClient(
        model=os.getenv("LLM_MODEL"), 
        api_key="ollama", 
        base_url=os.getenv("LLM_BASE_URL"),
        model_info={
            "vision": False,
            "function_calling": False,
            "json_output": False,
            "structured_output": False,
            "family": "unknown"
        }
    )

    # Init Team
    planner = get_planner_agent(model_client)
    worker = get_worker_agent(model_client)
    refiner = get_refiner_agent(model_client)
    validator = get_validator_agent(model_client)

    print("\n" + "="*50)
    print("MULTI-AGENT PLANNER-EXECUTOR TERMINAL (DAY 2)")
    print("Type 'quit' or 'exit' to end the session.")
    print("="*50)

    while True:
        user_query = input("\nEnter the task you want to perform: ").strip()
        
        # Handling Empty or Exit Queries
        if not user_query:
            print("Error: Query cannot be empty. Please try again.")
            continue
        
        if user_query.lower() in ['exit', 'quit']:
            print("Terminating session. Goodbye.")
            break

        start_total = time.perf_counter()

        try:
            # PHASE 1: PLANNING (The Architect)
            print(f"\n[1/4] ARCHITECT: Drafting strategic plan...")
            s1 = time.perf_counter()
            plan_res = await planner.on_messages([TextMessage(content=user_query, source="user")], None)
            plan_text = plan_res.chat_message.content
            e1 = time.perf_counter()
            
            print("-" * 30)
            print("PLANNER :")
            print(plan_text.strip())
            print("-" * 30)

            missions = re.findall(r"\[MISSION\]:.*", plan_text)
            if not missions:
                print("Planner Error: No valid missions identified in blueprint.")
                continue
                
            print(f"Planning completed in {e1-s1:.2f}s. {len(missions)} tasks found.")

            # PHASE 2: EXECUTION (The Specialists)
            print(f"\n[2/4] WORKERS: Executing missions (tasks) in parallel...")
            sw = time.perf_counter()
            worker_tasks = [
                worker.on_messages([TextMessage(content=m, source="planner")], None)
                for m in missions
            ]
            worker_results = await asyncio.gather(*worker_tasks)
            worker_contents = [r.chat_message.content for r in worker_results]
            
            # Print Raw Specialist Data for transparency
            for i, content in enumerate(worker_contents):
                print(f"--- WORKER {i+1} DATA ---\n{content.strip()}\n")
            
            print(f"Execution phase finished in {time.perf_counter()-sw:.2f}s.")

            # PHASE 3: REFINEMENT (The Editor)
            print(f"\n[3/4] EDITOR: Weaving and polishing raw data...")
            sr = time.perf_counter()
            refine_input = f"User Request: {user_query}\n\nWorker Data:\n" + "\n\n".join(worker_contents)
            refine_res = await refiner.on_messages([TextMessage(content=refine_input, source="workers")], None)
            final_draft = refine_res.chat_message.content
            
            print("-" * 40)
            print("REFINER'S POLISHED DRAFT:")
            print(final_draft.strip())
            print("-" * 40)
            
            print(f"Refinement finished in {time.perf_counter()-sr:.2f}s.")

            # PHASE 4: VALIDATION (The Mentor)
            print(f"\n[4/4] VALIDATION MENTOR: Reviewing final quality...")
            sv = time.perf_counter()
            val_res = await validator.on_messages([TextMessage(content=final_draft, source="refiner")], None)
            verdict = val_res.chat_message.content
            
            if "STATUS: APPROVED" in verdict:
                print(f"\nPLAN APPROVED (Review Time: {time.perf_counter()-sv:.2f}s)")
                print("="*60)
                print(verdict.replace("STATUS: APPROVED", "").strip())
                print("="*60)
            else:
                print(f"\nPLAN REJECTED: {verdict.replace('STATUS: REJECTED', '').strip()}")

            print(f"\nTOTAL PIPELINE TIME: {time.perf_counter() - start_total:.2f}s")

        except Exception as e:
            print(f"\nCRITICAL PIPELINE ERROR: {e}")

    await model_client.close()

if __name__ == "__main__":
    asyncio.run(main())