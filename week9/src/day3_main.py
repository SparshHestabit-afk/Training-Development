import json
import re
from groq import Groq
from dotenv import load_dotenv

from tools.file_agent import FileAgent
from tools.code_agent import CodeAgent
from tools.db_agent import DBAgent

# SETUP
load_dotenv()
client = Groq()
MODEL_NAME = "llama-3.3-70b-versatile"
#  creating an agent registry, for planner to choose agent based on task
AGENTS = {
    "file_agent": FileAgent(),
    "code_agent": CodeAgent(),
    "db_agent": DBAgent()
}

# this functionality is used for dynamic name fetching for databsae, based on user query, where it removes symbols, numbers, and common words, 
# to extract main database, which is then used for name resolution and connection, where user doesn't have to specify db name explicitly, 
def get_main_entity(query):
    query = query.lower()
    words = re.findall(r"[a-zA-Z]+", query) # extract all words
    action_words = {
        "create", "insert", "select", "update", "delete", "drop", "show", "analyse" # remove action words FIRST (important)
    }
    words = [w for w in words if w not in action_words]
    stopwords = {
        "table", "into", "from", "for", "a", "db", "database", "data", "entries", "the", "all" # remove other noise
    }
    words = [w for w in words if w not in stopwords]  # checks if all the words are not stopwords, if not then keep it, otherwise remove it
    if not words:
        return None
    return "_".join(words[:2]) # take first 2 clear words for naming convention, and join with underscore, resulting in database name

# PLANNER PROMPT (using JSON for clear structure, as it generates a plan in a sequential manner, prevents hallucination)
PLANNER_PROMPT = """
        You are an AI planner. Return ONLY a JSON array.

        FORMAT:
        [{"agent": "...", "action": "...", "args": {...}}] 

        AGENTS:
        - code_agent: run_python
        - file_agent: create_file, write_file, read_file
        - db_agent: execute_sql

        ROUTING:
        - SQL → db_agent
        - CSV/Python → code_agent
        - Files → file_agent

        DB:
        - SQLite only, use PRAGMA table_info for schema
        - Use real column names and values (no '?')
        - if inserting, when defined in the query , add N number of rows,

        CSV → DB:
        - ONLY if explicitly requested
        - Use pandas + sqlite3 (no SQLAlchemy)
        - CSV: src/files/data/<file>
        - DB: src/files/databases/<name>.db

        CODE:
        - Executable Python only
        - No unnecessary functions

        STRICT:
        - No explanations
        - Valid JSON only
    """

# UTIL
# this a simple reusable funciton, which calls the llm with a given message, and returns the response,
#  this is used in multiple places in the code, for better code organization and reusability, and also to 
# have a single place to modify if we want to change the way we call the llm in future
def call_llm(messages):
    res = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=0
    )
    return res.choices[0].message.content.strip()

# cleaning because llm often return a formatted response with md , so it cleans that to make it executable
def clean_output(text):
    text = text.replace("```python", "")
    text = text.replace("```", "")
    text = text.replace("<|python_tag|>", "")
    return text.strip()

# this function is responsible for building user messaege, incase of sql query , where we want to pass the schema of 
# the database as context to llm, so it can generate better plan and code, this is done by extracting main entity from query,
# then fetching schema using PRAGMA, and then appending that to user message with instructions.
def build_user_message(query):
    schema_text = ""
    try:
        entity = get_main_entity(query)
        if entity:
            db_agent = AGENTS["db_agent"] # this calls the db_agent to connect to the database,.

            # ensure DB connection, to access the schema for the connected database
            db_agent.connect(f"{entity}.db")
            schema = db_agent.execute_sql(f"PRAGMA table_info({entity})") # PRAGMA is a command, which return the metadata about the table

            if schema.get("success") and schema.get("result"):
                cols = [col["name"] for col in schema["result"]] # create a list of columns, extracting only name from the metadata
                schema_text = f"Table: {entity}\nColumns: {', '.join(cols)}" # foramtted schema, which has the name of all the columns in the table

    except Exception:
        # fail silently (important as it doesn't break the code)
        pass
    # FINAL USER MESSAGE (building the context for the llm, to understand the query better, and plan according to it
    user_message = f"User Query:\n{query}"

    if schema_text:
        user_message += f"""
            Database Context:
            {schema_text}

            Instructions:
            - Use this schema only if relevant
            - Do NOT invent column names
            - Avoid inserting primary keys or ID columns unless needed
        """
    return user_message

# PLANNER
def create_plan(query):
    # Code-only query → skip tools (bypass planning and go straight to code execution)
    if "code" in query.lower() and "file" not in query.lower():
        return []
    
    user_message = build_user_message(query) # final message with schema context if available, otherwise just user query

    raw = call_llm([
        {"role": "system", "content": PLANNER_PROMPT},
        {"role": "user", "content": user_message}
    ])

    raw = clean_output(raw) # cleaning the response to make it executable, removing any formatting or md tags
    try:
        plan = json.loads(raw) # converting to make it python ready
        # FIX: string inside list
        if isinstance(plan, list) and len(plan) > 0 and isinstance(plan[0], str): # ensures the plan is in correct format, where the first element is not string , so that it can be parser into json object
            plan = [json.loads(plan[0])]

        # validate structure (ensures that the plan is in correct format, LIST)
        if not isinstance(plan, list): 
            raise ValueError

        # validates each step in the plan, to ensure it has all the needed fields, and is in correct format
        for step in plan:
            if not isinstance(step, dict):
                raise ValueError
            if "agent" not in step or "action" not in step:
                raise ValueError

        return plan #return the final structure plan, which is a list of steps, where each step is a dictionary with agent, action and args

    except Exception:
        # fallback (in case of plan parsing failure , it return a default plan)
        return [{
            "agent": "code_agent",
            "action": "run_python",
            "args": {"task": query}
        }]

# EXECUTION
def execute_with_loop(plan, query):
    # CODE-ONLY CASE
    if not plan:
        print("\n[INFO] Code-only task detected")
        # calling llm to generate code for the given query
        code = call_llm([
            {"role": "system", "content": "Return ONLY Python code"},
            {"role": "user", "content": query}
        ])
        return [clean_output(code)] # returning the cleaned code as final response in a list format for consistency with tool-based output

    results = [] # list to store outputs from each step

    for idx, step in enumerate(plan):
        print(f"\n[STEP {idx+1}]")
        print("\n[PLAN STEP]")
        print(step)

        # fetches the needed parameters for tool execution, using ,get to avoid key error
        agent_name = step.get("agent")
        action = step.get("action")
        args = step.get("args", {})

        # Central DB routing logic (if SQL detected but no db_name provided)
        entity = get_main_entity(query)
        if "db_name" not in args:
            if "database" in args:
                args["db_name"] = args["database"]
            elif entity: # in case db does not exist, it creates a new db automatically
                args["db_name"] = f"{entity}.db"

        # STRICT VALIDATION (in case of llm creating a new agent)
        if agent_name not in AGENTS:
            return [f"Unknown agent: {agent_name}"]

        agent = AGENTS[agent_name]

        print(f"\n[TOOL CALL] {agent_name} → {action}") # defining which agent and action is being called

        try:
            result = agent.handle_task( # calls agent to perform action
                {"action": action, "args": args},
                query,
                client,
                MODEL_NAME
            )
        except Exception as e:
            return [f"Tool failed: {e}"]

        print("\n[TOOL RESULT]")
        print(result)

        results.append(result) # adding it to the list of output from each step

        # SPECIAL: PY FILE HANDLING (it creates a .py file, with code in it)
        if action == "create_file" and args.get("filename", "").endswith(".py"):
            code = call_llm([
                {"role": "system", "content": "Return ONLY Python code"},
                {"role": "user", "content": query}
            ])  

            file_agent = AGENTS["file_agent"] # calls the file agent to write the generated code into the file

            write_result = file_agent.handle_task({
                "action": "write_file",
                "args": {
                    "filename": args["filename"],
                    "content": clean_output(code)
                }
            }, query, client, MODEL_NAME)

            print("\n[CODE WRITTEN]")
            print(write_result)

            return [result, write_result] # returns both the file creation result and code writing result as final output

    return results # returns the list of outputs from all the steps in the plan as final output

def is_analysis_query(query): # checks if the query is related to analysis or insights
    keywords = [
        "analyze", "analysis", "insight",
        "pattern", "trend", "correlation",
        "summary", "statistics"
    ]
    return any(word in query.lower() for word in keywords)

def generate_insights(data): # function for creating the insights from the analysis output
    prompt = f"""
        You are a data analyst.
        The following is raw analysis output:
        {data}

        Your job is to:
        - Extract meaningful patterns ONLY
        - Ignore incorrect, trivial, or misleading statements
        - Ignore any references to ID-like fields
        - Ignore generic correlation statements

        Generate 3–5 high-quality insights, unless number of insights is specified in query

        Rules:
        - Do NOT repeat input text
        - Do NOT mention "correlation between X and Y" or any other datafrane related generic statements
        - Focus on real-world meaning and implications
        - Avoid assumptions if data is unclear

        Output:
        Top Insights:
        1. ...
        2. ...
        3. ...
        
    """
    return call_llm([
        {
            "role": "system",
            "content": "You are a data analyst generating high-quality insights."
        },
        {
            "role": "user",
            "content": prompt
        }
    ])

# RUN
def run(query):
    print("\n[PLANNING]")
    plan = create_plan(query)
    print(plan)

    print("\n[EXECUTION]")
    result = execute_with_loop(plan, query)

    if is_analysis_query(query):
        print("\n=== INSIGHTS ===")

        # extract last meaningful output
        final = result[-1] if isinstance(result, list) else result # retrieves the last output from the list , as it is the final output for our query

        if isinstance(final, dict): # tries to extract the main data from the final output, which can vary from agent to agent
            data = final.get("output") or final.get("result") or str(final)
        else:
            data = str(final) # if final output is not a dict, it converts it to string for insight generation

        try:
            insights = generate_insights(data) # calls the insight generation fucntion to create insights from the final output
            print(insights)
        except Exception as e:
            print(f"Insight generation failed: {e}")
            print("\n=== RAW OUTPUT ===")
            print(result) # incase it fails, it give the final output witout insights

    print("\n=== FINAL OUTPUT ===")
    print(result) # final response in the form of list of outputs from each step

    return result

# CLI
if __name__ == "__main__":
    print("Day-3 Tool Agent System")
    while True:
        q = input("\n>> ")
        if q.lower() == "exit":
            break
        run(q)
