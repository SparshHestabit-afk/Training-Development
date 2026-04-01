import os

from dotenv import load_dotenv
from autogen_ext.models.openai import OpenAIChatCompletionClient

# Nexus AI CORE CONFIGURATION
load_dotenv()
# 1. Initializing the MODEL_CLIENT (Optimized for Groq Llama-3)
MODEL_NAME = "llama-3.3-70b-versatile"
# MODEL_NAME = "llama-3.1-8b-instant"
# Groq provides the high-speed inference required for (9-agents) orchestration

MODEL_CLIENT = OpenAIChatCompletionClient(
    model = MODEL_NAME,
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
    model_info={
        "vision":False,
        "function_calling":True,
        "json_output":True,
        "family": "llama-3.3-70b",
        "structured_output":False
    }
)

# 2. Global Runtime Settings
# These LLM settings ensure stability across the multi-agent execution, controlling llm behaviour
LLM_CONFIG = {
    "cache_seed": 42,    # Ensures reproducible results during testing (same output for same input)
    "temperature": 0.3,   # Low temperature for high logical consistency
    "timeout": 120,    # Max time for LLM response to avoid slow working agents
    # "max_tokens": 2048, # Max tokens for response to ensure detailed outputs withoutexeceding model token limit
}

# These are the system settings to ensure efficient working for multi-agent execution
MAX_RETRIES = 2           # For failure recovery loop
ENABLE_LOGGING = True     # enable logging mechanism
ENABLE_MEMORY = True      # enable memory for recall and providing an extra layer of context to agents
ENABLE_TOOLS = True       # For coder agent, allowing use of multiple functionalities

# 3. Path Configuration for logging and memory and storing the newly created files
# Globasl or base directory settings
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Log Directory 
LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

# Workspace directory
WORKSPACE_DIR = os.path.join(BASE_DIR, "workspace")
os.makedirs(WORKSPACE_DIR, exist_ok=True)

# 4. Tools Settings for coder agent
TOOL_CONFIG = {
    "code_execution": True,
    "file_access": True
}

# 5. Logging Format
def get_log_file(step_name):
    import datetime

    # Logging based on timestamp for each step in the execution cycle
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_step = step_name.replace(" ", "_").lower()

    return os.path.join(LOG_DIR, f"{timestamp}_{safe_step}.txt")