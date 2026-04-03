import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import streamlit as st
from PIL import Image

from src.memory.memory_store import MemoryStore
from src.evaluation.rag_eval import RAGEvaluator
from src.generator.llm_client import LLMClient

from src.pipelines.sql_pipeline import SQLPipeline
from src.retriever.hybrid_retriever import HybridRetriever
from src.retriever.image_search import ImageSearch


# ----------------------------------
# CONFIG
# ----------------------------------

st.set_page_config(page_title="Enterprise Multimodal RAG", layout="wide")
st.title("Enterprise Multimodal RAG System")


# ----------------------------------
# SESSION STATE
# ----------------------------------

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# ----------------------------------
# LOAD SYSTEM
# ----------------------------------

@st.cache_resource
def load_system():

    memory = MemoryStore()
    evaluator = RAGEvaluator()
    llm = LLMClient()

    retriever = HybridRetriever()
    image_search = ImageSearch()

    db_config = {
        "host": "localhost",
        "port": 5432,
        "database": "music_db",
        "user": "postgres",
        "password": "postgres"
    }

    sql_pipeline = SQLPipeline(db_config)

    return memory, evaluator, llm, retriever, image_search, sql_pipeline


memory, evaluator, llm, retriever, image_search, sql_pipeline = load_system()


# ----------------------------------
# SIDEBAR (ALL CONTROLS)
# ----------------------------------

endpoint = st.sidebar.selectbox(
    "Select Endpoint",
    ["/ask", "/ask-image", "/ask-sql"]
)

st.sidebar.markdown("---")

# -------- CHAT HISTORY --------
st.sidebar.subheader("Chat History")

history_container = st.sidebar.container(height=300)

with history_container:
    history = st.session_state.chat_history[-5:]

    if len(history) == 0:
        st.info("No history yet")

    for chat in history:
        role = "🧑" if chat["role"] == "user" else "🤖"
        st.markdown(f"**{role}:** {chat['content']}")

st.sidebar.markdown("---")

# -------- FEEDBACK --------
st.sidebar.subheader("Feedback")

feedback = st.sidebar.text_area(
    "Improve system",
    placeholder="Give general feedback..."
)

if st.sidebar.button("Submit Feedback"):
    if feedback.strip():
        memory.save_feedback("global", "system", feedback)
        st.sidebar.success("Saved")


# ----------------------------------
# MAIN PANEL
# ----------------------------------

mode = None
if endpoint == "/ask-image":
    st.subheader("Image RAG Modes")

    mode = st.radio(
        "Select Mode",
        ["Text → Image", "Image → Image", "Image → Text"]
    )


# FIXED LABEL WARNING HERE ✅
st.subheader("Ask your question")
question = st.text_input(
    "Enter your question",
    label_visibility="collapsed"
)

uploaded_image = None
if endpoint == "/ask-image":
    uploaded_image = st.file_uploader("Upload Image")


# ----------------------------------
# SELF REFLECTION
# ----------------------------------

def refine_answer(question, context, answer):

    prompt = f"""
You are a strict evaluator and editor.

Question:
{question}

Context:
{context}

Answer:
{answer}

Tasks:
1. Remove unsupported parts
2. Improve clarity
3. Do NOT add external info
4. Keep it grounded

Return only final answer.
"""
    return llm.generate(prompt)


# ----------------------------------
# EXECUTION
# ----------------------------------

if st.button("Submit") and question:

    with st.spinner("Processing..."):

        context = ""
        trace = {}

        st.session_state.chat_history.append({
            "role": "user",
            "content": question
        })

        # ---------------- TEXT ----------------
        if endpoint == "/ask":

            docs = retriever.retrieve(question, top_k=5)

            context = "\n\n".join([d["text"] for d in docs])

            answer = llm.generate(f"""
Context:
{context}

Question:
{question}
""")

            trace["documents"] = docs

        # ---------------- IMAGE ----------------
        elif endpoint == "/ask-image":

            if mode == "Text → Image":

                results = image_search.search_by_text(question)

                cols = st.columns(3)
                for i, r in enumerate(results):
                    with cols[i % 3]:
                        st.image(r["image_path"], caption=r.get("caption", ""))

                st.stop()

            elif mode == "Image → Image":

                if uploaded_image is None:
                    st.warning("Upload image first")
                    st.stop()

                results = image_search.search_by_image(uploaded_image)

                cols = st.columns(3)
                for i, r in enumerate(results):
                    with cols[i % 3]:
                        st.image(r["image_path"], caption=r.get("caption", ""))

                st.stop()

            elif mode == "Image → Text":

                if uploaded_image is None:
                    st.warning("Upload image first")
                    st.stop()

                # ✅ FIX: Convert to PIL Image
                image = Image.open(uploaded_image).convert("RGB")

                answer = image_search.generate_caption(image)

                context = answer
                trace["image_caption"] = answer

        # ---------------- SQL ----------------
        elif endpoint == "/ask-sql":

            result = sql_pipeline.run(question)

            answer = result["summary"]
            context = result["summary"]

            trace["sql"] = result["sql"]

        # ---------------- REFINE ----------------
        if context:
            answer = refine_answer(question, context, answer)

        # ---------------- EVAL ----------------
        evaluation = evaluator.evaluate(question, context, answer)
        confidence = evaluation["faithfulness_score"]

        memory.save_interaction(question, answer, confidence, trace)

        st.session_state.chat_history.append({
            "role": "assistant",
            "content": answer
        })


    # ---------------- OUTPUT ----------------

    st.subheader("Answer")
    st.write(answer)

    st.write(f"Confidence: {confidence:.2f}")

    if evaluation["hallucinated"]:
        st.warning("⚠ Possible hallucination")

    with st.expander("Debug"):
        st.json(trace)

    with st.expander("Evaluation"):
        st.json(evaluation)