"""
FusionGPT — Resume Builder Page
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
from utils.api import inject_global_css, require_auth, render_sidebar_user, api_resume, page_header

st.set_page_config(page_title="Resume Builder — FusionGPT", page_icon="📄", layout="wide", initial_sidebar_state="expanded")
inject_global_css()
require_auth()
render_sidebar_user()

page_header("📄", "Resume Builder", "Generate ATS-friendly resume content — summaries, bullet points & skills")

col_in, col_out = st.columns([1, 1], gap="large")

with col_in:
    st.markdown("#### 👤 Your Information")

    job_title = st.text_input(
        "Target Job Title",
        placeholder="e.g. Senior Data Scientist, Full Stack Developer",
        key="res_title",
    )

    years_exp = st.slider(
        "Years of Experience",
        min_value=0, max_value=30, value=3,
        key="res_years",
    )

    key_skills = st.text_area(
        "Key Skills (comma-separated)",
        height=100,
        placeholder="e.g. Python, Machine Learning, TensorFlow, SQL, Data Visualization, Agile",
        key="res_skills",
    )

    recent_role = st.text_input(
        "Most Recent Role / Company",
        placeholder="e.g. Data Analyst at Google",
        key="res_role",
    )

    achievements = st.text_area(
        "Key Achievements / Responsibilities (optional)",
        height=130,
        placeholder="List your key wins and responsibilities, e.g.:\n• Led a team of 5 engineers to deliver a $2M product on time\n• Reduced churn by 15% through predictive modeling",
        key="res_achievements",
    )

    build_btn = st.button("📄 Build Resume Content →", use_container_width=True, key="res_btn")

with col_out:
    st.markdown("#### 📋 Generated Resume Content")
    result_placeholder = st.empty()

    if build_btn:
        if not job_title.strip():
            result_placeholder.error("Please enter your target job title.")
        elif not key_skills.strip():
            result_placeholder.error("Please enter at least a few key skills.")
        else:
            with st.spinner("📄 Crafting your resume content..."):
                try:
                    result = api_resume(
                        job_title=job_title,
                        years_experience=years_exp,
                        key_skills=key_skills,
                        recent_role=recent_role,
                        achievements=achievements if achievements.strip() else None,
                    )
                    resume_content = result["resume_content"]
                    tokens = result.get("tokens_used", 0)

                    result_placeholder.markdown(resume_content)
                    st.markdown(f'<span class="token-badge">⚡ {tokens} tokens</span>', unsafe_allow_html=True)
                    st.text_area("Copy resume content:", value=resume_content, height=200, key="res_copy")
                except ValueError as e:
                    result_placeholder.error(f"❌ {e}")
    else:
        result_placeholder.markdown(
            '<div class="output-box" style="color:#475569; text-align:center; padding:5rem 1rem;">Your resume content will appear here 📄</div>',
            unsafe_allow_html=True,
        )
