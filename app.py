import streamlit as st
import time
import google.generativeai as genai

from prompts import agri_prompt

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AgriShield AI Assistant",
    layout="centered"
)

# ---------------- STYLING ----------------
st.markdown("""
<style>
body {
    background: linear-gradient(180deg,#f2f2f4,#e6e7ea);
    color: #1e1e1e;
}

.title {
    text-align: center;
    margin-top: 60px;
}

.subtitle {
    color: #555;
    font-size: 1.1rem;
}

.chat-user {
    background: rgba(0,0,0,0.08);
    padding: 14px;
    border-radius: 16px;
    margin-top: 20px;
    text-align: right;
}

.chat-ai {
    background: rgba(255,255,255,0.6);
    backdrop-filter: blur(10px);
    padding: 14px;
    border-radius: 16px;
    margin-top: 10px;
}

.ask-btn {
    background: #2b2b2b !important;
    color: white !important;
    border-radius: 30px !important;
    padding: 10px 28px !important;
    border: none;
    font-size: 1rem;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("## 🔐 Setup")

    api_key = st.text_input(
        "Enter Gemini API Key",
        type="password",
        placeholder="Paste your Gemini API key"
    )

    location = st.text_input(
        "Your Location",
        placeholder="Village / Mandal / District"
    )

    st.markdown("---")
    st.caption("AgriShield uses your location to give relevant insights.")

# ---------------- TITLE ----------------
st.markdown("""
<div class="title">
    <h1>🌾 AgriShield AI Assistant</h1>
    <p class="subtitle">
        Ask questions about weather, crop prices, and mandi trends
    </p>
</div>
""", unsafe_allow_html=True)

# ---------------- QUESTION INPUT ----------------
question = st.text_input(
    "",
    placeholder="Ask your question here…"
)

ask = st.button("Ask AgriShield", key="ask")

# ---------------- VALIDATION ----------------
if ask and not api_key:
    st.warning("⚠️ Please enter your Gemini API key in the sidebar.")
    st.stop()

if ask and not location:
    st.warning("⚠️ Please enter your location in the sidebar.")
    st.stop()

if ask and not question:
    st.warning("⚠️ Please enter a question.")
    st.stop()

# ---------------- AI RESPONSE (FINAL WORKING PART) ----------------
if ask and api_key and location and question:

    # Show user message
    st.markdown(
        f"<div class='chat-user'>{question}</div>",
        unsafe_allow_html=True
    )

    with st.spinner("AgriShield is thinking..."):
        time.sleep(0.8)

        # Configure Gemini SDK
        genai.configure(api_key=api_key)

        model = genai.GenerativeModel("gemini-1.0-pro")

        prompt = agri_prompt(location, question)

        response = model.generate_content(prompt)

        st.markdown(
            f"<div class='chat-ai'>{response.text}</div>",
            unsafe_allow_html=True
    )
    # Show AI response
    st.markdown(
        f"<div class='chat-ai'>{response.text}</div>",
        unsafe_allow_html=True
    )
