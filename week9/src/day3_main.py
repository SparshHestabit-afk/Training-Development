import json
from groq import Groq
from dotenv import load_dotenv

from tools.file_agent import FileAgent
from tools.code_agent import CodeAgent
from tools.db_agent import DBAgent

# =========================
# SETUP
# =========================
load_dotenv()
client = Groq()
MODEL_NAME = "llama-3.3-70b-versatile"

AGENTS = {
    "file_agent": FileAgent(),
    "code_agent": CodeAgent(),
    "db_agent": DBAgent()
}

# =========================
# PROMPTS
# =========================
PLANNER_PROMPT = """
You are an AI planner.

STRICT RULES:

- Return ONLY a JSON array
- NO explanation
- NO markdown

FORMAT:

[
  {
    "agent": "code_agent",
    "action": "run_python",
    "args": {"task": "..."}
  }
]

VALID AGENTS:
- file_agent
- code_agent
- db_agent

VALID ACTIONS:

code_agent:
- run_python

file_agent:
- create_file
- write_file
- read_file

db_agent:
- execute_sql

CRITICAL:
- NEVER use custom function names
- NEVER return "code_agent.run_python"
- NEVER return strings
- NEVER return unknown agents like "data_agent"
- ALWAYS return structured JSON objects

RULES:

1. CSV → use code_agent.run_python
2. Python file → file_agent
3. SQL → db_agent
4. If unsure → code_agent.run_python
"""

EXECUTION_PROMPT = """
You are an execution agent.

STRICT RULES:

- ONLY return JSON
- NO explanation
- NO markdown
- NO ``` blocks

FORMAT:

Tool:
{
  "action": "tool",
  "agent": "...",
  "tool_action": "...",
  "args": {}
}

Final:
{
  "action": "final",
  "answer": "..."
}
"""

# =========================
# UTIL
# =========================
def call_llm(messages):
    res = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=0
    )
    return res.choices[0].message.content.strip()


def clean_output(text):
    text = text.replace("```python", "")
    text = text.replace("```", "")
    text = text.replace("<|python_tag|>", "")
    return text.strip()


def is_code_output(text):
    return "def " in text or "import " in text


# =========================
# PLANNER
# =========================
def create_plan(query):

    # Code-only query → skip tools
    if "code" in query.lower() and "file" not in query.lower():
        return []

    raw = call_llm([
        {"role": "system", "content": PLANNER_PROMPT},
        {"role": "user", "content": query}
    ])

    raw = clean_output(raw)

    try:
        plan = json.loads(raw)

        # 🔥 FIX: string inside list
        if isinstance(plan, list) and len(plan) > 0 and isinstance(plan[0], str):
            plan = [json.loads(plan[0])]

        # validate structure
        if not isinstance(plan, list):
            raise ValueError

        for step in plan:
            if not isinstance(step, dict):
                raise ValueError
            if "agent" not in step or "action" not in step:
                raise ValueError

        return plan

    except:
        # fallback
        return [{
            "agent": "code_agent",
            "action": "run_python",
            "args": {"task": query}
        }]


# =========================
# TOOL LOOP
# =========================
def execute_with_loop(plan, query):

    # =========================
    # CODE-ONLY CASE
    # =========================
    if not plan:
        print("\n[INFO] Code-only task detected")

        code = call_llm([
            {"role": "system", "content": "Return ONLY Python code"},
            {"role": "user", "content": query}
        ])

        return [clean_output(code)]

    messages = [
        {"role": "system", "content": EXECUTION_PROMPT},
        {"role": "system", "content": f"PLAN:\n{plan}"},
        {"role": "user", "content": query}
    ]

    results = []

    # =========================
    # 🔥 JSON EXTRACTOR (FINAL)
    # =========================
    def extract_json(text):
        start = text.find("{")
        if start == -1:
            return None

        stack = 0
        for i in range(start, len(text)):
            if text[i] == "{":
                stack += 1
            elif text[i] == "}":
                stack -= 1

            if stack == 0:
                return text[start:i+1]

        return None

    # =========================
    # LOOP
    # =========================
    for step in range(10):

        print(f"\n[STEP {step+1}]")

        raw = call_llm(messages)
        content = clean_output(raw)

        print("\n[LLM OUTPUT]")
        print(content)

        # =========================
        # 🔥 PARSE OUTPUT (FIXED)
        # =========================
        json_str = extract_json(content)

        if not json_str:
            return [f"❌ No valid JSON found:\n{content}"]

        try:
            action = json.loads(json_str)
        except Exception as e:
            return [f"❌ Invalid JSON:\n{json_str}\nError: {str(e)}"]

        # =========================
        # FINAL RESPONSE
        # =========================
        if action.get("action") == "final":
            return results + [action.get("answer")]

        # =========================
        # TOOL EXECUTION
        # =========================
        if action.get("action") == "tool" or "agent" in action:

            # normalize formats like "code_agent.run_python"
            if "." in str(action.get("action")):
                agent_name, tool_action = action["action"].split(".")
            else:
                agent_name = action.get("agent")
                tool_action = action.get("tool_action")

            args = action.get("args", {})

            # block invalid agents
            if agent_name not in AGENTS:
                return [f"❌ Unknown agent: {agent_name}"]

            # fix misuse
            if agent_name == "code_agent" and tool_action == "create_file":
                agent_name = "file_agent"

            if tool_action == "create_file":
                args.pop("content", None)

            agent = AGENTS[agent_name]

            print(f"\n[TOOL CALL] {agent_name} → {tool_action}")

            try:
                result = agent.handle_task(
                    {"action": tool_action, "args": args},
                    query,
                    client,
                    MODEL_NAME
                )
            except Exception as e:
                return [f"❌ Tool failed: {e}"]

            print("\n[TOOL RESULT]")
            print(result)

            results.append(result)

            # =========================
            # SPECIAL: PY FILE HANDLING
            # =========================
            if tool_action == "create_file" and args.get("filename", "").endswith(".py"):

                code = call_llm([
                    {"role": "system", "content": "Return ONLY Python code"},
                    {"role": "user", "content": query}
                ])

                file_agent = AGENTS["file_agent"]

                write_result = file_agent.handle_task({
                    "action": "write_file",
                    "args": {
                        "filename": args["filename"],
                        "content": clean_output(code)
                    }
                }, query, client, MODEL_NAME)

                print("\n[CODE WRITTEN]")
                print(write_result)

                return [result, write_result]

            # =========================
            # FEEDBACK LOOP
            # =========================
            messages.append({"role": "assistant", "content": json_str})
            messages.append({
                "role": "system",
                "content": f"Tool result:\n{result}"
            })

        else:
            return ["❌ Invalid action format"]

    return ["⚠️ Max steps reached"]
# =========================
# RUN
# =========================
def run(query):

    print("\n[PLANNING]")
    plan = create_plan(query)
    print(plan)

    print("\n[EXECUTION]")
    result = execute_with_loop(plan, query)

    print("\n=== FINAL OUTPUT ===")
    print(result)

    return result


# =========================
# CLI
# =========================
if __name__ == "__main__":

    print("Day-3 Tool Agent (Final Stable System)")

    while True:
        q = input("\n>> ")

        if q.lower() == "exit":
            break

        run(q)