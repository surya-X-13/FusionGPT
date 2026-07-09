"""
FusionGPT — Code Generator Page
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
from utils.api import inject_global_css, require_auth, render_sidebar_user, api_code, page_header

st.set_page_config(page_title="Code Generator — FusionGPT", page_icon="💻", layout="wide", initial_sidebar_state="expanded")
inject_global_css()
require_auth()
render_sidebar_user()

page_header("💻", "Code Generator", "Generate clean, production-ready code or get explanations in any language")

LANGUAGES = [
    "Python", "JavaScript", "TypeScript", "Java", "C", "C++", "C#", "Go",
    "Rust", "Swift", "Kotlin", "PHP", "Ruby", "R", "MATLAB", "SQL",
    "Bash/Shell", "PowerShell", "Dart", "Scala", "HTML/CSS", "React (JSX)",
    "Vue.js", "Node.js",
]

# ── Mode selector ─────────────────────────────────────────────────────────────
task_mode = st.radio(
    "Mode",
    ["🛠️ Generate Code", "🔍 Explain Code"],
    horizontal=True,
    label_visibility="collapsed",
    key="code_mode",
)
task = "generate" if "Generate" in task_mode else "explain"

col_in, col_out = st.columns(2, gap="large")

with col_in:
    language = st.selectbox("Programming Language", LANGUAGES, key="code_lang")

    if task == "generate":
        st.markdown("#### 📋 Describe What to Build")
        description = st.text_area(
            "What should the code do?",
            height=280,
            placeholder="E.g. 'A function that takes a list of integers and returns them sorted using merge sort, with type hints and docstring'",
            label_visibility="collapsed",
            key="code_desc",
        )
        code_to_explain = None
    else:
        st.markdown("#### 🔍 Paste Code to Explain")
        code_to_explain = st.text_area(
            "Code to explain",
            height=280,
            placeholder="Paste your code here...",
            label_visibility="collapsed",
            key="code_explain_input",
        )
        description = f"Explain this {language} code"

    generate_btn = st.button(
        f"{'⚡ Generate Code' if task == 'generate' else '🔍 Explain Code'} →",
        use_container_width=True,
        key="code_btn",
    )

with col_out:
    st.markdown("#### 🖥️ Output")
    result_placeholder = st.empty()

    if generate_btn:
        if not description.strip() and not code_to_explain:
            result_placeholder.error("Please provide a description or code to process.")
        else:
            action = "Generating code" if task == "generate" else "Analyzing code"
            with st.spinner(f"💻 {action}..."):
                try:
                    result = api_code(
                        description=description,
                        language=language,
                        task=task,
                        code_to_explain=code_to_explain,
                    )
                    output = result["result"]
                    tokens = result.get("tokens_used", 0)
                    result_placeholder.markdown(output)
                    st.markdown(f'<span class="token-badge">⚡ {tokens} tokens · {language}</span>', unsafe_allow_html=True)
                    st.text_area("Copy output:", value=output, height=150, key="code_copy")
                except ValueError as e:
                    result_placeholder.error(f"❌ {e}")
    else:
        result_placeholder.markdown(
            '<div class="output-box" style="color:#475569; text-align:center; padding:5rem 1rem;">Generated code will appear here 💻</div>',
            unsafe_allow_html=True,
        )
