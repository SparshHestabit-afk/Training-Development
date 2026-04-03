import streamlit as st
import requests

# ------------------------------------------------
# CONFIG
# ------------------------------------------------

API_URL = "http://localhost:8000"

st.set_page_config(page_title="Local LLM", layout="wide")

# ------------------------------------------------
# TITLE
# ------------------------------------------------

st.title("Local LLM Interface")

# ------------------------------------------------
# SESSION MEMORY (IMPORTANT)
# ------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# ------------------------------------------------
# HEALTH CHECK
# ------------------------------------------------

def check_api_health():
    try:
        response = requests.get(f"{API_URL}/health", timeout=2)
        return response.status_code == 200
    except:
        return False

api_ok = check_api_health()

if api_ok:
    st.success("API is running")
else:
    st.error("API not reachable. Start FastAPI backend.")

# ------------------------------------------------
# SIDEBAR SETTINGS
# ------------------------------------------------

st.sidebar.header("Settings")

temperature = st.sidebar.slider("Temperature", 0.0, 1.5, 0.7)
top_p = st.sidebar.slider("Top P", 0.0, 1.0, 0.9)
top_k = st.sidebar.slider("Top K", 1, 100, 50)
max_tokens = st.sidebar.slider("Max Tokens", 10, 512, 150)

mode = st.sidebar.radio("Mode", ["Generate", "Chat"])

system_prompt = st.sidebar.text_area(
    "System Prompt",
    value="You are a DevOp AI assistant. Give explanation and examples"
)

# ------------------------------------------------
# INPUT AREA
# ------------------------------------------------

st.subheader("Enter Prompt")

user_input = st.text_area("Your Input", height=150)

generate_btn = st.button("Generate")

# ------------------------------------------------
# DISPLAY CHAT HISTORY (NEW)
# ------------------------------------------------

if mode == "Chat" and st.session_state.messages:
    st.subheader("Conversation")

    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"**User:** {msg['content']}")
        else:
            st.markdown(f"**Assistant:** {msg['content']}")

# ------------------------------------------------
# STREAM FUNCTION
# ------------------------------------------------

def stream_response(endpoint, payload):
    try:
        response = requests.post(endpoint, json=payload, stream=True)

        if response.status_code != 200:
            yield f"API Error: {response.status_code}"
            return

        for chunk in response.iter_content(chunk_size=512):
            if chunk:
                yield chunk.decode("utf-8", errors="ignore")

    except Exception as e:
        yield f"Error: {str(e)}"

# ------------------------------------------------
# OUTPUT AREA
# ------------------------------------------------

if generate_btn:

    if not api_ok:
        st.error("Backend API is not running.")
        st.stop()

    if not user_input.strip():
        st.warning("Please enter a prompt.")
        st.stop()

    st.subheader("Response")

    output_box = st.empty()
    full_response = ""

    # ------------------------------
    # Mode selection
    # ------------------------------

    if mode == "Chat":

        # Save user message
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })

        payload = {
            "system_prompt": system_prompt,
            "user_message": user_input,
            "temperature": temperature,
            "top_p": top_p,
            "top_k": top_k
        }

        endpoint = f"{API_URL}/chat"

    else:
        payload = {
            "prompt": user_input + "\n\nExplain in detail with examples.",
            "temperature": temperature,
            "top_p": top_p,
            "top_k": top_k,
            "max_tokens": max_tokens
        }

        endpoint = f"{API_URL}/generate"

    # ------------------------------
    # Streaming Output
    # ------------------------------

    with st.spinner("Generating..."):
        for chunk in stream_response(endpoint, payload):
            full_response += chunk
            output_box.markdown(full_response.strip())

    output_box.markdown(full_response.strip())

    # Save assistant response (ONLY for chat)
    if mode == "Chat":
        st.session_state.messages.append({
            "role": "assistant",
            "content": full_response
        })