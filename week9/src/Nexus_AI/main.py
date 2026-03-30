import json
import asyncio
import re

from config import (
    MODEL_CLIENT,
    MAX_RETRIES,
    ENABLE_MEMORY,
    ENABLE_LOGGING,
    ENABLE_TOOLS,
    get_log_file
)

from memory_manager import MemoryManager

from agents.orchestrator_agent import get_orchestrator
from agents.planner_agent import get_planner
from agents.research_agent import get_researcher
from agents.analyst_agent import get_analyst
from agents.coder_agent import get_coder
from agents.critic_agent import get_critic
from agents.optimizer_agent import get_optimizer
from agents.validator_agent import get_validator
from agents.reporter_agent import get_reporter

# =========================
# INITIALIZING 
# =========================
memory = MemoryManager() if ENABLE_MEMORY else None
log_buffer = []

# =========================
# LOGGING FUNCTIONS
# =========================
def log_step(step, content):
    if ENABLE_LOGGING:
        log_buffer.append(f"\n[{step}]\n{content}\n")

def save_log():
    if ENABLE_LOGGING:
        file_path = get_log_file("nexus_run")
        with open(file_path, "w") as f:
            f.write("\n".join(log_buffer))

# =========================
# UTIL (TOKEN LIMITING)
# ========================
def trim(text, max_chars=2000):
    return text[-max_chars:] if text else ""

# =========================
# INTENT CLASSIFIER (FOR user query )
# =========================
def classify_intent(query):
    q = query.lower()

    if any(k in q for k in ["my name is", "i am", "i live", "remember"]):
        return "memory"

    if any(k in q for k in [
        "what is my", "who am i", "what did i",
        "do you remember", "what do you know about me"
    ]):
        return "memory_query"

    if len(q.split()) <= 3:
        return "simple"

    return "task"

# =========================
# MEMORY ENHANCEMENT
# =========================
def enrich_memory(query):
    data = {}

    name_match = re.search(r"my name is (.+)", query.lower())
    if name_match:
        data["name"] = name_match.group(1).strip()

    return data

# =========================
# DEFINING TOOL SYSTEM
# =========================
def build_tools(query=None):
    if not ENABLE_TOOLS:
        return None

    from tools.code_tool import CodeTool
    from tools.file_tool import FileTool

    code_tool = CodeTool()
    file_tool = FileTool()

    def run_code(code: str = "") -> str:
        if not code:
            return "NO CODE PROVIDED"
        return code_tool.run(code)

    def save_file(filename: str, content: str) -> str:
        return file_tool.save_file(filename, content)

    def read_file(filename: str) -> str:
        return file_tool.read(filename)

    return [run_code, save_file, read_file]

# =========================
# INITIALIZING AGENTS
# =========================
def build_agents(query=None):
    tools = build_tools(query)

    return {
        "Orchestrator": get_orchestrator(MODEL_CLIENT),
        "Planner": get_planner(MODEL_CLIENT),
        "Researcher": get_researcher(MODEL_CLIENT),
        "Analyst": get_analyst(MODEL_CLIENT),
        "Coder": get_coder(MODEL_CLIENT, tools=tools),
        "Critic": get_critic(MODEL_CLIENT),
        "Optimizer": get_optimizer(MODEL_CLIENT),
        "Validator": get_validator(MODEL_CLIENT),
        "Reporter": get_reporter(MODEL_CLIENT),
    }

# =========================
# MAIN ENGINE
# =========================
async def run_query(query):

    print("\nNEXUS AI STARTED...")

    agents = build_agents(query)
    original_query = query

    # =========================
    # MEMORY CONTEXT
    # =========================
    if memory:
        print("\n[MEMORY] Retrieving context...")
        messages = memory.retrieve(original_query)
        memory_context = "\n".join(
            [m["content"] for m in messages if m["role"] == "system"]
        )
        query = f"""
            USER QUERY:
            {original_query}

            MEMORY CONTEXT:
            {memory_context}
        """

    # =========================
    # ORCHESTRATOR CALLING
    # =========================
    print("\n[ORCHESTRATOR] Generating sequence...")

    result = await agents["Orchestrator"].run(task=query)
    raw_output = result.messages[-1].content.strip()

    try:
        agent_sequence = json.loads(raw_output)

    except:
        try:
            match = re.search(r"\[.*\]", raw_output, re.DOTALL)
            if match:
                agent_sequence = json.loads(match.group())
            else:
                raise ValueError
        except:
            print("Orchestrator fallback triggered....!!")
            agent_sequence = ["Planner", "Analyst", "Validator", "Reporter"]

    # filter valid agents
    valid_agents = {
        "Planner", "Researcher", "Analyst",
        "Coder", "Critic", "Optimizer",
        "Validator", "Reporter"
    }
    
    # double checking the sequence 
    agent_sequence = [a for a in agent_sequence if a in valid_agents]
    if not agent_sequence:
        agent_sequence = ["Reporter"]

    print("Agent Flow:", agent_sequence)

    # avoiding unnecessary coder agent calling
    if "code" not in original_query.lower():
        agent_sequence = [a for a in agent_sequence if a != "Coder"]

    # =========================
    # EXECUTION LOOP
    # =========================
    context = query
    attempt = 0

    while attempt <= MAX_RETRIES:

        print(f"\n Attempt {attempt+1}")

        for agent_name in agent_sequence:

            agent = agents.get(agent_name)
            if not agent:
                continue

            print(f"\n[{agent_name}] Running...")
            context = f"""
                USER QUERY:
                {original_query}

                CURRENT CONTEXT:
                {context}
            """

            try:
                result = await agent.run(task=trim(context))
                output = result.messages[-1].content

                # coder retry (in case of failure)
                if agent_name == "Coder":
                    retry_count = 0
                    while any(err in output.lower() for err in ["error", "traceback", "exception"]) and retry_count < MAX_RETRIES:
                        retry_count += 1
                        print(f"Code failed → retrying ({retry_count}/{MAX_RETRIES})")
                        retry_result = await agent.run(task=trim(context))
                        output = retry_result.messages[-1].content

            except Exception as e:
                output = f"ERROR: {str(e)}"

            log_step(agent_name, output)
            context = trim(output)

            # validator agent calling, peforming final validation check
            if agent_name == "Validator":
                if "REJECT" in output.upper() and attempt < MAX_RETRIES:
                    print("Validation failed --> retrying.........")
                    attempt += 1
                    break
                else:
                    print("Validation passed....!!")
        else:
            break

    # =========================
    # FINAL RESPONSE
    # =========================
    print("\n[REPORTER] Generating final output...")

    result = await agents["Reporter"].run(
        task=f"""
            Answer the USER QUERY clearly and directly.

            USER QUERY:
            {original_query}

            CONTEXT:
            {context}
        """
    )
    final_output = result.messages[-1].content
    log_step("FINAL_OUTPUT", final_output)

    if memory:
        print("\n[MEMORY] Storing interaction...")
        memory.store(original_query, final_output)

    save_log()

    return final_output

# =========================
# CLI
# =========================
if __name__ == "__main__":

    print("NEXUS AI SYSTEM READY....")

    while True:
        q = input("-->> ").strip()
        if q.lower() == "exit":
            break
        if q.lower() == "quit":
            break

        # clear memory
        if memory and q.lower() in ["clear all", "clear session", "clear long", "clear vector"]:
            print("\n=== RESPONSE ===")
            print(memory.clear(q.lower()))
            continue

        intent = classify_intent(q)

        # =========================
        # MEMORY STORE
        # =========================
        if intent == "memory":
            print("\nMemory detected")

            info = enrich_memory(q)
            if memory:
                if info:
                    memory.store(q, f"USER_DATA: {info}")
                else:
                    memory.store(q, q)

            print("Got it! I'll remember that.")
            continue

        # =========================
        # MEMORY QUERY (GENERIC)
        # =========================
        if intent == "memory_query":
            print("\n Memory Query Detected")

            if memory:
                mem = memory.retrieve(q)
                agents = build_agents(q)

                result = asyncio.run(
                    agents["Reporter"].run(
                        task=f"""
                            Answer using ONLY MEMORY.

                            USER QUERY:
                            {q}

                            MEMORY:
                            {mem}

                            If not found, say you don't know.
                        """
                    )
                )
                print(result.messages[-1].content)
            continue

        # =========================
        # SIMPLE (for instant reply to simple query/questions)
        # =========================
        if intent == "simple":
            print("\n⚡ Simple query detected")
            agents = build_agents(q)
            result = asyncio.run(agents["Reporter"].run(task=q))
            print(result.messages[-1].content)
            continue

        # =========================
        # FULL PIPELINE (MAIN CALL)
        # =========================
        try:
            result = asyncio.run(run_query(q))
            print("\n========== FINAL OUTPUT ==========\n")
            print(result)

        except Exception as e:
            print("\nERROR:", str(e))