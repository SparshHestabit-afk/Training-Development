from autogen_agentchat.agents import AssistantAgent
from autogen_core.model_context import BufferedChatCompletionContext

def get_reporter(MODEL_CLIENT):

    context = BufferedChatCompletionContext(buffer_size=5)

    return AssistantAgent(
        name = "Reporter_Agent",
        model_client=MODEL_CLIENT,
        model_context=context,
        system_message="""
            You are the Nexus AI Reporter.
            Your job is to present the final output to the user in a clear and user-ready format.

            RULES:
            - Answer directly and clearly based on the USER QUERY
            - Use the provided context as the source of truth
            - Incorporate relevant information from context naturally
            - Do NOT change or reinterpret factual results
            - Do NOT add missing information
            - Do NOT include system details, logs, or process explanations

            STYLE:
            - Clear and natural response
            - Structured only if helpful (bullets, steps, code blocks)
            - Keep it concise but complete

            This is the final response shown to the user.
            Output only the final answer.
        """
    )