import streamlit as st
from google import genai

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Farmer AI Assistant 🌾",
    page_icon="🌱",
    layout="centered"
)

st.title("🌾 Farmer AI Assistant")
st.subheader("Location-based agriculture guidance using AI")

# ---------------- STYLING ----------------
st.markdown("""
<style>

/* Main app background */
.stApp {
    background: linear-gradient(180deg, #0f172a 0%, #020617 100%);
    color: #e5e7eb;
    font-family: "Inter", sans-serif;
}

/* Title section */
.title {
    text-align: center;
    margin-top: 40px;
}

.title h1 {
    font-size: 2.2rem;
    font-weight: 700;
    color: #f9fafb;
}

.subtitle {
    color: #9ca3af;
    font-size: 1.05rem;
}

/* User chat bubble */
.chat-user {
    background: linear-gradient(135deg, #2563eb, #1d4ed8);
    color: #ffffff;
    padding: 14px 18px;
    border-radius: 18px 18px 4px 18px;
    margin-top: 20px;
    margin-left: auto;
    max-width: 75%;
    box-shadow: 0 8px 18px rgba(37, 99, 235, 0.45);
    font-size: 0.95rem;
}

/* AI chat bubble */
.chat-ai {
    background: rgba(30, 41, 59, 0.85);
    color: #e5e7eb;
    padding: 14px 18px;
    border-radius: 18px 18px 18px 4px;
    margin-top: 12px;
    max-width: 75%;
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.6);
    backdrop-filter: blur(12px);
    font-size: 0.95rem;
    line-height: 1.6;
}

/* Input fields */
input[type="text"], textarea {
    background-color: #020617 !important;
    color: #f9fafb !important;
    border-radius: 12px !important;
    padding: 10px 14px !important;
    border: 1px solid #334155 !important;
    font-size: 0.95rem !important;
}

input::placeholder, textarea::placeholder {
    color: #64748b !important;
}

/* Primary button */
.stButton > button {
    background: linear-gradient(135deg, #22c55e, #16a34a);
    color: #022c22;
    border-radius: 999px;
    padding: 10px 28px;
    border: none;
    font-size: 0.95rem;
    font-weight: 600;
    box-shadow: 0 8px 18px rgba(34, 197, 94, 0.45);
    transition: all 0.2s ease-in-out;
}

.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 12px 26px rgba(34, 197, 94, 0.6);
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #020617, #020617);
    border-right: 1px solid #1e293b;
}

section[data-testid="stSidebar"] h2 {
    color: #f9fafb;
    font-weight: 600;
}

/* Hide Streamlit footer */
footer {
    visibility: hidden;
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

    language = st.selectbox(
        "Response Language",
        ["English", "Hindi", "Telugu", "Tamil", "Kannada"]
    )

    st.markdown("---")
    st.caption("AgriShield uses your location to give relevant insights.")

# ---------------- TITLE ----------------
st.markdown("""
<div class="title">
    <h1>🌾 AgriShield AI Assistant</h1>
    <p class="subtitle">
        Ask agriculture questions and get farmer-friendly answers
    </p>
</div>
""", unsafe_allow_html=True)

# ---------------- QUESTION INPUT ----------------
question = st.text_input(
    "",
    placeholder="Ask your agriculture question here…"
)

ask = st.button("🌱 Ask AgriShield", key="ask")

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

# ---------------- AI RESPONSE ----------------
if ask and api_key and location and question:

    # Show user message
    st.markdown(
        f"<div class='chat-user'>{question}</div>",
        unsafe_allow_html=True
    )

    with st.spinner("AgriShield is thinking..."):

        # ✅ Create Gemini client
        client = genai.Client(api_key=api_key)

        prompt = f"""
You are an agriculture expert helping Indian farmers.

Location: {location}
Question: {question}

Instructions:
- Give location-specific advice
- Use simple farmer-friendly language
- Avoid technical words
- Respond in {language}
"""

        try:
            response = client.models.generate_content(
                model="models/gemini-flash-latest",
                contents=prompt
            )

            # Show AI response
            st.markdown(
                f"<div class='chat-ai'>{response.text}</div>",
                unsafe_allow_html=True
            )

        except Exception as e:
            st.error(f"Error: {e}")

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("🌍 AI-powered agriculture support for farmers")
