"""
FusionGPT — Text Summarizer Page
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
from utils.api import inject_global_css, require_auth, render_sidebar_user, api_summarize, page_header

st.set_page_config(page_title="Summarizer — FusionGPT", page_icon="📝", layout="wide", initial_sidebar_state="expanded")
inject_global_css()
require_auth()
render_sidebar_user()

page_header("📝", "Text Summarizer", "Condense any text into a clear, concise summary in seconds")

col_in, col_out = st.columns(2, gap="large")

with col_in:
    st.markdown("#### ✍️ Input Text")
    text_input = st.text_area(
        "Paste your text here",
        height=350,
        placeholder="Paste an article, document, paragraph, or any long text here...",
        label_visibility="collapsed",
        key="sum_input",
    )
    length = st.select_slider(
        "Summary Length",
        options=["short", "medium", "long"],
        value="medium",
        help="Short = 2-3 sentences | Medium = 1-2 paragraphs | Long = detailed",
    )
    word_count = len(text_input.split()) if text_input else 0
    st.caption(f"📊 {word_count} words · {len(text_input)} characters")
    summarize_btn = st.button("✨ Summarize →", use_container_width=True, key="sum_btn")

with col_out:
    st.markdown("#### 📋 Summary")
    result_placeholder = st.empty()

    if summarize_btn:
        if not text_input.strip():
            result_placeholder.error("Please enter some text to summarize.")
        elif len(text_input.strip()) < 50:
            result_placeholder.error("Text must be at least 50 characters.")
        else:
            with st.spinner("📝 Summarizing..."):
                try:
                    result = api_summarize(text_input, length)
                    summary = result["summary"]
                    tokens = result.get("tokens_used", 0)
                    result_placeholder.markdown(
                        f'<div class="output-box">{summary}</div>',
                        unsafe_allow_html=True,
                    )
                    st.markdown(f'<span class="token-badge">⚡ {tokens} tokens · {len(summary.split())} words</span>', unsafe_allow_html=True)

                    # Copy helper
                    st.text_area("Copy summary:", value=summary, height=100, key="sum_copy_area")
                except ValueError as e:
                    result_placeholder.error(f"❌ {e}")
    else:
        result_placeholder.markdown(
            '<div class="output-box" style="color:#475569; text-align:center; padding:5rem 1rem;">Your summary will appear here ✨</div>',
            unsafe_allow_html=True,
        )
