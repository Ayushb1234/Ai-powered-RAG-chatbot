import streamlit as st
from file_parser import extract_text
from rag_pipeline import build_faiss_index, rag_response, load_knowledge_base
from chatbot import generate_response
import os

# --- PAGE SETUP ---
st.set_page_config(page_title="💬 RAG Chatbot", layout="centered")
st.title("💬 AI Chatbot with Dynamic Knowledge Base (RAG)")
st.markdown("Upload a PDF, DOCX, or TXT file. Then ask anything about its content!")

# --- SESSION STATE SETUP ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- KNOWLEDGE BASE UPLOAD ---
kb_file = st.file_uploader("📚 Upload Knowledge Base", type=["pdf", "docx", "txt"])

if kb_file:
    kb_text = extract_text(kb_file)
    if kb_text and len(kb_text.strip()) > 10:
        st.success("✅ Knowledge base loaded successfully!")
        with st.expander("📄 View Extracted Text"):
            st.write(kb_text)
        chunks = load_knowledge_base(kb_text)   # 🔁 Fix here
        index, _ = build_faiss_index(chunks)    # Now send list of chunks

        st.session_state["index"] = index
        st.session_state["kb_text"] = kb_text
        st.session_state["chunks"] = chunks 
    else:
        st.warning("⚠️ File seems empty or unreadable.")

# --- MODEL SELECTION ---
st.markdown("### 🧠 Choose a Language Model")
selected_model = st.selectbox("Select a model for answering:", [
    # "sentence-transformers/all-MiniLM-L6-v2",
    "google/flan-t5-base",
    # "mistralai/Mistral-7B-Instruct-v0.1"
    "bigscience/bloom-560m",  # ✅ Public
    "tiiuae/falcon-rw-1b"  
])
st.session_state["selected_model"] = selected_model  # Save selection

# --- CHAT INPUT ---
st.markdown("---")
user_input = st.text_input("🗨️ Ask something based on the knowledge base:")

# --- RESPONSE GENERATION ---
if st.button("Ask"):
    if user_input and "index" in st.session_state:
        with st.spinner("🤖 Generating answer..."):
            context = rag_response(user_input, st.session_state["index"], st.session_state["chunks"], st.session_state["selected_model"])
            prompt = f"Context:\n{context}\n\nQuestion: {user_input}"
            response = generate_response(prompt, st.session_state["selected_model"])

            # Save chat history
            st.session_state.chat_history.append(("You", user_input))
            st.session_state.chat_history.append(("Bot", response))
    elif not kb_file:
        st.warning("📂 Please upload a knowledge base first.")
    elif not user_input:
        st.warning("📝 Please type your query.")

# --- CHAT HISTORY DISPLAY ---
if st.session_state.chat_history:
    st.markdown("### 💬 Chat History")
    for role, message in reversed(st.session_state.chat_history[-10:]):  # last 10 exchanges
        st.markdown(f"**{role}:** {message}")
