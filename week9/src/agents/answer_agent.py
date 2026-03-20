from autogen_agentchat.agents import AssistantAgent
from autogen_core.model_context import BufferedChatCompletionContext

def get_answer_agent(MODEL_CLIENT):
    # can be changed to 10, according to our original requirement
    context = BufferedChatCompletionContext(buffer_size=2)

    return AssistantAgent(
        name = "Answer_Agent",
        model_client=MODEL_CLIENT,
        model_context=context,
        system_message="""
ROLE: Answer Generator
TASK: Take the summarized data or processed info from the Summary_Agent, and generate a final answer (formatted).
CONSTRAINT: Provide only final answer, which is based on the summarize facts, not adding extra data or info. You are the RESPONSE LAYER,
whose job is to to create a clear, easy-to-read, professional response for the user, which carries a helpful and highly-readable text, solely based  on the summary.
"""
    )