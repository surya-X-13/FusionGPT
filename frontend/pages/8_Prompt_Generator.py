"""
FusionGPT — Prompt Generator Page
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
from utils.api import inject_global_css, require_auth, render_sidebar_user, api_prompt, page_header

st.set_page_config(page_title="Prompt Generator — FusionGPT", page_icon="🎯", layout="wide", initial_sidebar_state="expanded")
inject_global_css()
require_auth()
render_sidebar_user()

page_header("🎯", "Prompt Generator", "Engineer the perfect AI prompt for any task — get better results from any LLM")

st.markdown("""
<style>
.prompt-tip {
    background: rgba(245, 158, 11, 0.1);
    border: 1px solid rgba(245, 158, 11, 0.3);
    border-radius: 10px;
    padding: 0.75rem 1rem;
    font-size: 0.85rem;
    color: #FCD34D;
    margin-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="prompt-tip">💡 <strong>Pro Tip:</strong> Great prompts are specific, include context, desired format, and constraints. Our AI will craft all of this for you.</div>',
    unsafe_allow_html=True,
)

col_in, col_out = st.columns([1, 1], gap="large")

with col_in:
    st.markdown("#### 🎯 Your Goal")

    goal = st.text_area(
        "What do you want the AI to do?",
        height=160,
        placeholder="Describe your task or goal...\n\nExamples:\n• Write a product description for a wireless keyboard\n• Analyze the sentiment of customer reviews\n• Create a lesson plan for teaching Python to beginners",
        label_visibility="collapsed",
        key="prompt_goal",
    )

    context = st.text_area(
        "Background Context (optional)",
        height=120,
        placeholder="Any relevant context, constraints, or background...\nE.g. Target audience, industry, specific requirements",
        key="prompt_context",
    )

    output_format = st.text_input(
        "Desired Output Format (optional)",
        placeholder="e.g. Bullet points, JSON, step-by-step guide, markdown table",
        key="prompt_format",
    )

    # Quick examples
    st.markdown("**Quick examples:**")
    quick_examples = {
        "📊 Data Analysis": "Analyze sales data and identify trends",
        "✍️ Content Writing": "Write an engaging blog post introduction",
        "🎓 Education": "Explain quantum computing to a 10-year-old",
        "💼 Business": "Draft a professional business proposal",
    }
    ex_cols = st.columns(2)
    for i, (label, example_goal) in enumerate(quick_examples.items()):
        with ex_cols[i % 2]:
            if st.button(label, key=f"ex_{i}", use_container_width=True):
                st.session_state["prompt_goal"] = example_goal
                st.rerun()

    generate_btn = st.button("🎯 Generate Prompt →", use_container_width=True, key="prompt_btn")

with col_out:
    st.markdown("#### ⚡ Generated Prompt")
    result_placeholder = st.empty()

    if generate_btn:
        if not goal.strip():
            result_placeholder.error("Please describe your goal.")
        else:
            with st.spinner("🎯 Engineering your perfect prompt..."):
                try:
                    result = api_prompt(
                        goal=goal,
                        context=context if context.strip() else None,
                        output_format=output_format if output_format.strip() else None,
                    )
                    generated = result["generated_prompt"]
                    tokens = result.get("tokens_used", 0)

                    result_placeholder.markdown(generated)
                    st.markdown(f'<span class="token-badge">⚡ {tokens} tokens</span>', unsafe_allow_html=True)
                    st.text_area("Copy prompt:", value=generated, height=200, key="prompt_copy")
                except ValueError as e:
                    result_placeholder.error(f"❌ {e}")
    else:
        result_placeholder.markdown(
            '<div class="output-box" style="color:#475569; text-align:center; padding:5rem 1rem;">Your engineered prompt will appear here 🎯</div>',
            unsafe_allow_html=True,
        )
