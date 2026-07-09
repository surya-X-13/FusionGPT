"""
FusionGPT — AI Chatbot Page
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
from utils.api import inject_global_css, require_auth, render_sidebar_user, api_chat, page_header

st.set_page_config(page_title="Chatbot — FusionGPT", page_icon="💬", layout="wide", initial_sidebar_state="expanded")
inject_global_css()
require_auth()
render_sidebar_user()

# ── Extra styles ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
.chat-container {
    max-height: 500px;
    overflow-y: auto;
    padding: 1rem;
    background: rgba(10,10,20,0.5);
    border: 1px solid rgba(124,58,237,0.2);
    border-radius: 16px;
    margin-bottom: 1rem;
}
.chat-role-user { text-align: right; margin-bottom: 0.75rem; }
.chat-role-assistant { text-align: left; margin-bottom: 0.75rem; }
.chat-bubble-user {
    display: inline-block;
    background: linear-gradient(135deg, #7C3AED, #6D28D9);
    color: white;
    padding: 0.7rem 1.1rem;
    border-radius: 18px 18px 4px 18px;
    max-width: 80%;
    font-size: 0.95rem;
    line-height: 1.5;
}
.chat-bubble-ai {
    display: inline-block;
    background: linear-gradient(135deg, #1E1E35, #16213E);
    border: 1px solid rgba(124,58,237,0.3);
    color: #E2E8F0;
    padding: 0.7rem 1.1rem;
    border-radius: 18px 18px 18px 4px;
    max-width: 85%;
    font-size: 0.95rem;
    line-height: 1.6;
}
.chat-label { font-size: 0.75rem; color: #64748B; margin-bottom: 0.25rem; }
</style>
""", unsafe_allow_html=True)

page_header("💬", "AI Chatbot", "Have a natural conversation with your AI assistant — powered by Groq")

# ── Session state ─────────────────────────────────────────────────────────────
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "chat_display" not in st.session_state:
    st.session_state.chat_display = []

# ── Clear button ──────────────────────────────────────────────────────────────
col1, col2 = st.columns([5, 1])
with col2:
    if st.button("🗑 Clear", use_container_width=True):
        st.session_state.chat_history = []
        st.session_state.chat_display = []
        st.rerun()

# ── Chat display ──────────────────────────────────────────────────────────────
chat_html = '<div class="chat-container">'
if not st.session_state.chat_display:
    chat_html += '<div style="text-align:center; color:#475569; padding:2rem;">Send a message to start chatting 👇</div>'
else:
    for msg in st.session_state.chat_display:
        if msg["role"] == "user":
            chat_html += f'''
            <div class="chat-role-user">
                <div class="chat-label">You</div>
                <div class="chat-bubble-user">{msg["content"]}</div>
            </div>'''
        else:
            safe_content = msg["content"].replace("\n", "<br>")
            chat_html += f'''
            <div class="chat-role-assistant">
                <div class="chat-label">🤖 FusionGPT</div>
                <div class="chat-bubble-ai">{safe_content}</div>
            </div>'''
chat_html += "</div>"
st.markdown(chat_html, unsafe_allow_html=True)

# ── Input ──────────────────────────────────────────────────────────────────────
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_area(
        "Your message",
        placeholder="Ask me anything...",
        height=100,
        key="chat_input",
        label_visibility="collapsed",
    )
    submitted = st.form_submit_button("Send Message ➤", use_container_width=True)

if submitted and user_input.strip():
    with st.spinner("🤔 Thinking..."):
        try:
            result = api_chat(user_input.strip(), st.session_state.chat_history)
            reply = result["reply"]

            # Update history for API (keep last 10 turns to avoid context overflow)
            st.session_state.chat_history.append({"role": "user", "content": user_input.strip()})
            st.session_state.chat_history.append({"role": "assistant", "content": reply})
            st.session_state.chat_history = st.session_state.chat_history[-20:]

            # Update display
            st.session_state.chat_display.append({"role": "user", "content": user_input.strip()})
            st.session_state.chat_display.append({"role": "assistant", "content": reply})

            tokens = result.get("tokens_used", 0)
            st.caption(f"⚡ {tokens} tokens used")
            st.rerun()
        except ValueError as e:
            st.error(f"❌ {e}")
