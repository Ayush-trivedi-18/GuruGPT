import streamlit as st
from groq import Groq
import random

# --- 1. CONFIG ---
st.set_page_config(page_title="GuruGPT | Ayush Trivedi", page_icon="💎", layout="wide")

# --- 2. DYNAMIC PROMPT POOL ---
# These rotate automatically on every page refresh
PROMPT_POOL = [
    "🚀 What are the top 3 AI trends dominating 2026?",
    "📈 How is data analytics transforming the retail industry right now?",
    "💡 Give me a unique startup idea combining AI and sustainability.",
    "🐍 Write a Python script to automate a daily data cleaning task.",
    "🌍 Summarize the most recent breakthrough in space exploration.",
    "🧠 Explain the concept of 'Agentic AI' in simple terms.",
    "🎨 Suggest a creative prompt for an AI image generator.",
    "📊 How can a Data Analyst use LLMs to improve SQL query writing?",
    "🔬 What is the current state of Quantum Computing in 2026?",
    "⚡ Give me 5 tips to improve my productivity using AI tools."
]

# This picks 3 new ones every time the script runs (refresh)
current_prompts = random.sample(PROMPT_POOL, 3)

# --- 3. PREMIUM UI (Space Background & Glassmorphism) ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(125deg, #050505 0%, #0a0f1e 50%, #1a1033 100%);
        background-size: 400% 400%;
        animation: gradientBG 12s ease infinite;
        color: #ececf1;
    }
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .chat-header { text-align: center; margin-top: 50px; margin-bottom: 30px; }
    .chat-header h1 { font-size: 3.8rem; font-weight: 800; color: #ffffff; text-shadow: 0 0 20px rgba(59, 130, 246, 0.4); }

    /* Vertical Tile Buttons */
    .stButton>button {
        background: rgba(255, 255, 255, 0.03);
        color: #d1d5db;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 22px;
        width: 100%;
        max-width: 580px;
        margin: 10px auto;
        display: block;
        transition: 0.4s;
        text-align: center;
        backdrop-filter: blur(8px);
    }
    .stButton>button:hover {
        background: rgba(59, 130, 246, 0.15);
        border-color: #3b82f6;
        color: #ffffff;
        box-shadow: 0 0 20px rgba(59, 130, 246, 0.3);
        transform: translateY(-2px);
    }

    section[data-testid="stSidebar"] { background-color: #0d1117 !important; border-right: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. STATE MANAGEMENT ---
if "messages" not in st.session_state:
    st.session_state.messages = []

def handle_click(query):
    st.session_state.messages.append({"role": "user", "content": query})

# --- 5. SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='color: #3b82f6;'>Developer</h2>", unsafe_allow_html=True)
    st.write("### **Ayush Trivedi**")
    st.caption("Data Analyst @ NielsenIQ | AI Enthusiast")
    st.divider()
    st.link_button("🔗 LinkedIn Profile", "https://linkedin.com/in/YOUR_LINK", use_container_width=True)
    st.link_button("💻 GitHub Portfolio", "https://github.com/YOUR_USER", use_container_width=True)
    st.divider()
    st.caption("GuruGPT v5.0 | Powered by Groq")

# --- 6. CENTERED CONTENT (Welcome + Dynamic Prompts) ---
if not st.session_state.messages:
    st.markdown("""
        <div class="chat-header">
            <h1>💎 GuruGPT</h1>
            <p>Built by <b>Ayush Trivedi</b>. Dynamic. Intelligent. Fast.</p>
        </div>
        """, unsafe_allow_html=True)

    _, center_col, _ = st.columns([1, 2, 1])
    with center_col:
        for p in current_prompts:
            # We don't use on_click here to ensure the state updates correctly with the rerun
            if st.button(p):
                handle_click(p)
                st.rerun()

# --- 7. API ACCESS ---
if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    with st.sidebar.expander("🛠️ Admin Key"):
        temp_key = st.text_input("Enter Groq Key:", type="password")
        if temp_key: client = Groq(api_key=temp_key)
        else: st.stop()

# --- 8. CHAT INTERFACE ---
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="👤" if message["role"] == "user" else "🤖"):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask GuruGPT anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.rerun()

if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    with st.chat_message("assistant", avatar="🤖"):
        full_res = ""
        placeholder = st.empty()
        try:
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": "You are GuruGPT, a high-performance AI created by Ayush Trivedi, a Data Analyst at NielsenIQ. You are here to provide concise, smart, and professional answers."},
                    *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                ],
                stream=True
            )
            for chunk in completion:
                if chunk.choices[0].delta.content:
                    full_res += chunk.choices[0].delta.content
                    placeholder.markdown(full_res + "▌")
            placeholder.markdown(full_res)
            st.session_state.messages.append({"role": "assistant", "content": full_res})
        except Exception as e:
            st.error(f"Error: {e}")