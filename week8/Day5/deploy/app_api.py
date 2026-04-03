from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from deploy.model_loader import generate_response
from deploy.config import MAX_NEW_TOKENS

app = FastAPI()

# ------------------------------
# Memory
# ------------------------------

chat_history = []

# ------------------------------
# Schemas
# ------------------------------

class GenerateRequest(BaseModel):
    prompt: str
    temperature: float = 0.7
    top_p: float = 0.9
    top_k: int = 50
    max_tokens: int = MAX_NEW_TOKENS


class ChatRequest(BaseModel):
    system_prompt: str
    user_message: str
    temperature: float = 0.7
    top_p: float = 0.9
    top_k: int = 50


# ------------------------------
# Health
# ------------------------------

@app.get("/health")
def health():
    return {"status": "ok"}


# ------------------------------
# Generate (DETAILED OUTPUT)
# ------------------------------

@app.post("/generate")
def generate(req: GenerateRequest):

    prompt = f"""
<|system|>
You are a DevOps AI assistant. Give detailed answers with explanations and examples.

<|user|>
{req.prompt}

<|assistant|>
"""

    def stream():
        try:
            text = generate_response(
                prompt,
                req.temperature,
                req.top_p,
                req.top_k,
                req.max_tokens
            )

            yield text

        except Exception as e:
            yield f"Error: {str(e)}"

    return StreamingResponse(stream(), media_type="text/plain")


# ------------------------------
# Chat (INTERACTIVE MEMORY)
# ------------------------------

@app.post("/chat")
def chat(req: ChatRequest):

    # Save user message
    chat_history.append({"role": "user", "content": req.user_message})

    # Build full prompt
    full_prompt = f"<|system|>\n{req.system_prompt}\n"

    for msg in chat_history:
        if msg["role"] == "user":
            full_prompt += f"<|user|>\n{msg['content']}\n"
        else:
            full_prompt += f"<|assistant|>\n{msg['content']}\n"

    full_prompt += "<|assistant|>\n"

    def stream():
        try:
            text = generate_response(
                full_prompt,
                req.temperature,
                req.top_p,
                req.top_k,
                MAX_NEW_TOKENS
            )

            # Save assistant response
            chat_history.append({"role": "assistant", "content": text})

            yield text

        except Exception as e:
            yield f"Error: {str(e)}"

    return StreamingResponse(stream(), media_type="text/plain")