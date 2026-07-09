"""
FusionGPT — History Page
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
from utils.api import inject_global_css, require_auth, render_sidebar_user, api_history, api_stats, page_header

st.set_page_config(page_title="History — FusionGPT", page_icon="🕐", layout="wide", initial_sidebar_state="expanded")
inject_global_css()
require_auth()
render_sidebar_user()

page_header("🕐", "Usage History", "Review all your past AI interactions and usage statistics")

FEATURE_ICONS = {
    "chat": "💬", "summarize": "📝", "translate": "🌍",
    "code": "💻", "grammar": "✅", "email": "📧",
    "resume": "📄", "prompt": "🎯",
}
FEATURE_COLORS = {
    "chat": "#7C3AED", "summarize": "#EC4899", "translate": "#10B981",
    "code": "#F59E0B", "grammar": "#3B82F6", "email": "#EF4444",
    "resume": "#8B5CF6", "prompt": "#06B6D4",
}

# ── Stats strip ───────────────────────────────────────────────────────────────
try:
    stats = api_stats()
    c1, c2, c3 = st.columns(3)
    c1.metric("📊 Total Requests", stats["total_requests"])
    c2.metric("⚡ Total Tokens", f"{stats['total_tokens_used']:,}")
    breakdown = stats.get("feature_breakdown", {})
    top_feature = max(breakdown, key=breakdown.get) if breakdown else "—"
    c3.metric("🔥 Top Feature", f"{FEATURE_ICONS.get(top_feature, '🤖')} {top_feature.title()}")
except Exception:
    st.info("Could not load stats.")

st.markdown("---")

# ── Filters ───────────────────────────────────────────────────────────────────
col_filter1, col_filter2 = st.columns([2, 1])
with col_filter1:
    feature_filter = st.selectbox(
        "Filter by Feature",
        ["All Features", "chat", "summarize", "translate", "code", "grammar", "email", "resume", "prompt"],
        format_func=lambda x: f"{FEATURE_ICONS.get(x, '📊')} {x.title()}" if x != "All Features" else "📊 All Features",
        key="hist_filter",
    )
with col_filter2:
    limit = st.selectbox("Show Last", [25, 50, 100, 200], key="hist_limit")

feature_param = None if feature_filter == "All Features" else feature_filter

# ── Load history ──────────────────────────────────────────────────────────────
try:
    logs = api_history(limit=limit, feature=feature_param)
except ValueError as e:
    st.error(f"❌ {e}")
    logs = []

if not logs:
    st.markdown(
        '<div class="output-box" style="text-align:center; padding:3rem; color:#64748B;">No history found. Start using AI tools to see your history here! 🚀</div>',
        unsafe_allow_html=True,
    )
else:
    st.markdown(f"**Showing {len(logs)} interactions**")
    for log in logs:
        feature = log.get("feature", "unknown")
        icon = FEATURE_ICONS.get(feature, "🤖")
        color = FEATURE_COLORS.get(feature, "#7C3AED")
        created_at = log.get("created_at", "").replace("T", " ").split(".")[0]
        tokens = log.get("tokens_used", 0)

        input_text = log.get("input_text") or ""
        output_text = log.get("output_text") or ""

        with st.expander(
            f"{icon} **{feature.title()}** — {created_at} &nbsp;|&nbsp; ⚡ {tokens} tokens",
            expanded=False,
        ):
            if input_text:
                st.markdown(f"**Input:**")
                st.markdown(
                    f'<div class="output-box" style="border-color:{color}33; font-size:0.9rem;">'
                    f'{input_text[:500]}{"..." if len(input_text) > 500 else ""}</div>',
                    unsafe_allow_html=True,
                )
            if output_text:
                st.markdown("**Output:**")
                st.markdown(
                    f'<div class="output-box" style="font-size:0.9rem;">'
                    f'{output_text[:800]}{"..." if len(output_text) > 800 else ""}</div>',
                    unsafe_allow_html=True,
                )
            st.markdown(
                f'<span class="token-badge" style="background:rgba({int(color[1:3],16)},{int(color[3:5],16)},{int(color[5:7],16)},0.15);">⚡ {tokens} tokens used</span>',
                unsafe_allow_html=True,
            )
