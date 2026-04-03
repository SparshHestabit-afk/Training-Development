# from modern autogen_agentchat library we are importing AssistantAgent Class , 
# which actually is a blank wrapper, which is used to basically create an ai agent.
from autogen_agentchat.agents import AssistantAgent
# from modern autogen.core library we are importing BufferedChatCompletionContext method,
# which is implementing sliding context window, where we define the buffer size, which is actually no. of chat/response it remembers, and forgets the rest 
from autogen_core.model_context import BufferedChatCompletionContext

# MODEL_CLIENT is the configuration of our local LLM (qwen 2.5), which we are not defining it here, 
# to implement DEPENDECY INJECTION, which is in case of changes in configuration, only main has to be changes, 
# not all the realted files or dependencies
def get_research_agent(MODEL_CLIENT):
    # Each agent gets its own buffer of 2, this is to control and provide context memory window, and can be changed to 10.
    context = BufferedChatCompletionContext(buffer_size=2)
    
    return AssistantAgent(
        name = "Research_Agent",
        model_client=MODEL_CLIENT,
        model_context=context, 
        # we are using it (system_message) for role isolation, as LLM can be over-reaching, so using constraint,
        # we can define the exact working of the LLM in that file or scenario, binding its functionality
        system_message="""
ROLE: Professional Researcher.
TASK: Gather detailed facts, information and raw data on the defined (user's) topic.
CONSTRAINT: Provide only raw information and facts. Do not process/summarize or format them into final answer.You are the Perception Layer,
whose job is to gather detailed data and acurate facts about the specified topic, not generating a formatted response or the final output (drawing conclusion).
"""
    )