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
    background-color: #0f0f0f;
}

.title {
    text-align: center;
    margin-top: 80px;
}

.input-box {
    width: 100%;
    background: #1f1f1f;
    border-radius: 30px;
    padding: 14px;
    margin-top: 20px;
    border: 1px solid #333;
}

button {
    background: #4CAF50;
    color: white;
    border-radius: 25px;
    padding: 10px 25px;
    border: none;
    font-size: 1rem;
    margin-top: 15px;
    cursor: pointer;
}

.chat-user {
    background: #2b2b2b;
    padding: 14px;
    border-radius: 16px;
    margin-top: 20px;
    text-align: right;
}

.chat-ai {
    background: #1f1f1f;
    padding: 14px;
    border-radius: 16px;
    margin-top: 10px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.markdown("""
<div class="title">
    <h1>🌾 AgriShield AI Assistant</h1>
    <p>Ask questions about weather, crop prices, and nearby mandis</p>
</div>
""", unsafe_allow_html=True)

# ---------------- INPUTS ----------------
location = st.text_input(
    "Enter your location (Village / Mandal / District)",
    placeholder="e.g. Guntur, Andhra Pradesh"
)

question = st.text_input(
    "Ask your question",
    placeholder="e.g. Will it rain this week? What is today's paddy price?"
)

ask = st.button("Ask AgriShield")

# ---------------- VALIDATION ----------------
if ask and not location:
    st.warning("⚠️ Please enter your location before asking a question.")
    st.stop()

# ---------------- AI RESPONSE ----------------
if ask and location and question:

    st.markdown(f"<div class='chat-user'>{question}</div>", unsafe_allow_html=True)

    with st.spinner("AgriShield is thinking..."):
        time.sleep(1)

        payload = {
            "contents": [
                {"parts": [{"text": agri_prompt(location, question)}]}
            ]
        }

        response = requests.post(
            f"{GEMINI_ENDPOINT}?key={st.secrets['GEMINI_API_KEY'] if 'GEMINI_API_KEY' in st.secrets else ''}",
            headers={"Content-Type": "application/json"},
            json=payload
        )

    if response.status_code == 200:
        answer = response.json()["candidates"][0]["content"]["parts"][0]["text"]
        st.markdown(f"<div class='chat-ai'>{answer}</div>", unsafe_allow_html=True)
    else:
        st.error("Unable to fetch response. Please check API key or try again.")