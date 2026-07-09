"""
FusionGPT — Grammar Checker Page
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
from utils.api import inject_global_css, require_auth, render_sidebar_user, api_grammar, page_header

st.set_page_config(page_title="Grammar Checker — FusionGPT", page_icon="✅", layout="wide", initial_sidebar_state="expanded")
inject_global_css()
require_auth()
render_sidebar_user()

page_header("✅", "Grammar Checker", "Fix grammar, spelling, punctuation and polish your writing instantly")

col_in, col_out = st.columns(2, gap="large")

with col_in:
    st.markdown("#### ✍️ Your Text")
    text_input = st.text_area(
        "Enter text to check",
        height=380,
        placeholder="Paste your text here — essays, emails, reports, cover letters...\n\nExample: 'Their are many reasons why i thinks this is a good idea and we should of done it sooner.'",
        label_visibility="collapsed",
        key="gram_input",
    )
    word_count = len(text_input.split()) if text_input else 0
    char_count = len(text_input)
    st.caption(f"📊 {word_count} words · {char_count} characters")
    check_btn = st.button("✅ Check & Fix Grammar →", use_container_width=True, key="gram_btn")

with col_out:
    st.markdown("#### 📋 Corrected Text")
    result_placeholder = st.empty()

    if check_btn:
        if not text_input.strip():
            result_placeholder.error("Please enter some text.")
        elif len(text_input.strip()) < 10:
            result_placeholder.error("Text must be at least 10 characters.")
        else:
            with st.spinner("🔍 Checking grammar..."):
                try:
                    result = api_grammar(text_input)
                    corrected = result["corrected_text"]
                    tokens = result.get("tokens_used", 0)

                    result_placeholder.markdown(
                        f'<div class="output-box">{corrected.replace(chr(10), "<br>")}</div>',
                        unsafe_allow_html=True,
                    )
                    st.markdown(f'<span class="token-badge">⚡ {tokens} tokens</span>', unsafe_allow_html=True)

                    # Stats comparison
                    orig_words = len(text_input.split())
                    corr_words = len(corrected.split())
                    diff = corr_words - orig_words
                    diff_str = f"+{diff}" if diff > 0 else str(diff)
                    c1, c2 = st.columns(2)
                    c1.metric("Original Words", orig_words)
                    c2.metric("Corrected Words", corr_words, diff_str)

                    st.text_area("Copy corrected text:", value=corrected, height=120, key="gram_copy")
                except ValueError as e:
                    result_placeholder.error(f"❌ {e}")
    else:
        result_placeholder.markdown(
            '<div class="output-box" style="color:#475569; text-align:center; padding:5rem 1rem;">Corrected text will appear here ✅</div>',
            unsafe_allow_html=True,
        )
