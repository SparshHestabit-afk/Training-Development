from autogen_agentchat.agents import AssistantAgent
from autogen_core.model_context import BufferedChatCompletionContext

def get_summary_agent(MODEL_CLIENT):
    # can be changed to 10, according to our original requirement
    context = BufferedChatCompletionContext(buffer_size=2)
    
    return AssistantAgent(
        name = "Summary_Agent",
        model_client=MODEL_CLIENT,
        model_context= context,
        system_message="""
ROLE: Information Summarizer
TASK: Take the raw data from the Reaserch_Agent, process that data, and create a summary/conclusion from the raw facts.
CONSTRAINT: Provide only the summary, focusing on logic and reasoning. You are the REASONING Layer,
whose job is to preserve and summarize the logic and reasoning, removing redundant data or facts, and providing processed info.
"""
    )