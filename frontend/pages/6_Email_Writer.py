"""
FusionGPT — Email Writer Page
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
from utils.api import inject_global_css, require_auth, render_sidebar_user, api_email, page_header

st.set_page_config(page_title="Email Writer — FusionGPT", page_icon="📧", layout="wide", initial_sidebar_state="expanded")
inject_global_css()
require_auth()
render_sidebar_user()

page_header("📧", "Email Writer", "Draft professional, polished emails in seconds — just provide the context")

TONES = {
    "professional": "👔 Professional",
    "casual": "😊 Casual & Friendly",
    "apologetic": "🙏 Apologetic",
    "persuasive": "💡 Persuasive",
    "follow_up": "📬 Follow-Up",
}

col_in, col_out = st.columns([1, 1], gap="large")

with col_in:
    st.markdown("#### ⚙️ Email Details")

    tone_key = st.selectbox(
        "Tone",
        list(TONES.keys()),
        format_func=lambda k: TONES[k],
        key="email_tone",
    )

    recipient = st.text_input(
        "Recipient Name / Role",
        placeholder="e.g. HR Manager, John Smith, Team",
        key="email_recipient",
    )

    context = st.text_area(
        "Email Purpose / Context",
        height=180,
        placeholder="Describe what this email should communicate...\n\nExamples:\n• Request a meeting to discuss Q4 marketing strategy\n• Apologize for a delayed project delivery\n• Follow up on a job application sent last week",
        key="email_context",
    )

    additional = st.text_area(
        "Additional Details (optional)",
        height=100,
        placeholder="Any specific points, dates, or requirements to include...",
        key="email_additional",
    )

    write_btn = st.button("📧 Draft Email →", use_container_width=True, key="email_btn")

with col_out:
    st.markdown("#### 📬 Generated Email")
    result_placeholder = st.empty()

    if write_btn:
        if not context.strip():
            result_placeholder.error("Please describe the purpose of the email.")
        else:
            with st.spinner("✍️ Drafting your email..."):
                try:
                    result = api_email(
                        context=context,
                        recipient=recipient,
                        tone=tone_key,
                        additional_info=additional if additional.strip() else None,
                    )
                    email_content = result["email_content"]
                    tokens = result.get("tokens_used", 0)

                    result_placeholder.markdown(
                        f'<div class="output-box" style="white-space:pre-wrap;">{email_content}</div>',
                        unsafe_allow_html=True,
                    )
                    st.markdown(f'<span class="token-badge">⚡ {tokens} tokens · {TONES[tone_key]} tone</span>', unsafe_allow_html=True)
                    st.text_area("Copy email:", value=email_content, height=150, key="email_copy")
                except ValueError as e:
                    result_placeholder.error(f"❌ {e}")
    else:
        result_placeholder.markdown(
            '<div class="output-box" style="color:#475569; text-align:center; padding:5rem 1rem;">Your drafted email will appear here 📬</div>',
            unsafe_allow_html=True,
        )
