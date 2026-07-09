"""
FusionGPT — Translator Page
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
from utils.api import inject_global_css, require_auth, render_sidebar_user, api_translate, page_header

st.set_page_config(page_title="Translator — FusionGPT", page_icon="🌍", layout="wide", initial_sidebar_state="expanded")
inject_global_css()
require_auth()
render_sidebar_user()

page_header("🌍", "Translator", "Instantly translate text into 100+ languages with precision")

LANGUAGES = [
    "Arabic", "Bengali", "Bulgarian", "Chinese (Simplified)", "Chinese (Traditional)",
    "Croatian", "Czech", "Danish", "Dutch", "English", "Estonian", "Finnish",
    "French", "German", "Greek", "Gujarati", "Hebrew", "Hindi", "Hungarian",
    "Indonesian", "Italian", "Japanese", "Kannada", "Korean", "Latvian",
    "Lithuanian", "Malay", "Malayalam", "Marathi", "Norwegian", "Persian",
    "Polish", "Portuguese", "Punjabi", "Romanian", "Russian", "Serbian",
    "Slovak", "Slovenian", "Spanish", "Swahili", "Swedish", "Tamil", "Telugu",
    "Thai", "Turkish", "Ukrainian", "Urdu", "Vietnamese",
]

col_in, col_out = st.columns(2, gap="large")

with col_in:
    st.markdown("#### ✍️ Source Text")
    source_lang = st.selectbox("Source Language", ["Auto Detect"] + LANGUAGES, key="src_lang")
    text_input = st.text_area(
        "Text to translate",
        height=300,
        placeholder="Enter text to translate...",
        label_visibility="collapsed",
        key="trans_input",
    )
    word_count = len(text_input.split()) if text_input else 0
    st.caption(f"📊 {word_count} words")

with col_out:
    st.markdown("#### 🌐 Translation")
    target_lang = st.selectbox("Target Language", LANGUAGES, index=LANGUAGES.index("Spanish"), key="tgt_lang")
    result_placeholder = st.empty()

    translate_btn = st.button("🌍 Translate →", use_container_width=True, key="trans_btn")

    if translate_btn:
        if not text_input.strip():
            result_placeholder.error("Please enter text to translate.")
        else:
            src = "auto" if source_lang == "Auto Detect" else source_lang
            with st.spinner(f"Translating to {target_lang}..."):
                try:
                    result = api_translate(text_input, target_lang, src)
                    translated = result["translated_text"]
                    tokens = result.get("tokens_used", 0)
                    result_placeholder.markdown(
                        f'<div class="output-box">{translated}</div>',
                        unsafe_allow_html=True,
                    )
                    st.markdown(f'<span class="token-badge">⚡ {tokens} tokens · {target_lang}</span>', unsafe_allow_html=True)
                    st.text_area("Copy translation:", value=translated, height=100, key="trans_copy")
                except ValueError as e:
                    result_placeholder.error(f"❌ {e}")
    else:
        result_placeholder.markdown(
            '<div class="output-box" style="color:#475569; text-align:center; padding:5rem 1rem;">Translation will appear here 🌐</div>',
            unsafe_allow_html=True,
        )
