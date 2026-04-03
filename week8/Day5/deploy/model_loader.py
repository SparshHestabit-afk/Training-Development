from llama_cpp import Llama
from deploy.config import MODEL_PATH

print("Loading GGUF model...")

llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=2048,
    n_threads=8
)

print("Model loaded successfully")


def generate_response(prompt, temperature, top_p, top_k, max_tokens):

    output = llm(
        prompt,  
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=top_p,
        top_k=top_k,
        repeat_penalty=1.15,
        stop=["</s>", "<|user|>"]
    )

    return output["choices"][0]["text"].strip()