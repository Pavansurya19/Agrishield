import streamlit as st
import requests
import time

from prompts import agri_prompt
from config import GEMINI_ENDPOINT


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
        placeholder="Paste your API key here"
    )

    location = st.text_input(
        "Your Location",
        placeholder="Village / Mandal / District"
    )

    st.markdown("---")
    st.caption("AgriShield AI uses location to give relevant insights.")

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
    placeholder="Ask your question here…",
)

ask = st.button("Ask AgriShield", key="ask", help="Submit your question")

# ---------------- VALIDATION ----------------
if ask and not api_key:
    st.warning("⚠️ Please enter your API key in the sidebar.")
    st.stop()

if ask and not location:
    st.warning("⚠️ Please enter your location in the sidebar.")
    st.stop()

# ---------------- AI RESPONSE ----------------
if ask and api_key and location and question:

    st.markdown(f"<div class='chat-user'>{question}</div>", unsafe_allow_html=True)

    with st.spinner("AgriShield is thinking..."):
        time.sleep(1)

        payload = {
            "contents": [
                {"parts": [{"text": agri_prompt(location, question)}]}
            ]
        }

        response = requests.post(
            f"{GEMINI_ENDPOINT}?key={api_key}",
            headers={"Content-Type": "application/json"},
            json=payload
        )

    if response.status_code == 200:
        answer = response.json()["candidates"][0]["content"]["parts"][0]["text"]
        st.markdown(f"<div class='chat-ai'>{answer}</div>", unsafe_allow_html=True)
    else:
        st.error("Unable to fetch response. Please check your API key or quota.")
