"""
FusionGPT — Dashboard Page
Self-contained page (no wildcard imports to avoid duplicate set_page_config errors).
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
from utils.api import (
    inject_global_css,
    require_auth,
    render_sidebar_user,
    api_stats,
    get_logo_path,
)

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Dashboard — FusionGPT",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_global_css()
require_auth()
render_sidebar_user()

# ── Extra dashboard styles ─────────────────────────────────────────────────────
st.markdown("""
<style>
/* ---- Animated background gradient ---- */
.main { background: linear-gradient(135deg, #0a0a14 0%, #0f0f1e 50%, #0a0a14 100%) !important; }

/* ---- Stat cards (glassmorphism) ---- */
.stat-card {
    background: linear-gradient(135deg, rgba(26,26,46,0.9), rgba(22,33,62,0.85));
    border: 1px solid rgba(124,58,237,0.35);
    border-radius: 20px;
    padding: 1.75rem 1.5rem;
    text-align: center;
    position: relative;
    overflow: hidden;
    transition: all 0.3s ease;
    backdrop-filter: blur(10px);
}
.stat-card::before {
    content: "";
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle at center, rgba(124,58,237,0.08) 0%, transparent 70%);
    pointer-events: none;
}
.stat-card:hover {
    border-color: rgba(124,58,237,0.65);
    transform: translateY(-4px);
    box-shadow: 0 20px 50px rgba(124,58,237,0.2);
}
.stat-value {
    font-size: 2.8rem;
    font-weight: 900;
    background: linear-gradient(135deg, #A78BFA 0%, #EC4899 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1;
    margin-bottom: 0.4rem;
}
.stat-icon {
    font-size: 2rem;
    margin-bottom: 0.5rem;
    display: block;
}
.stat-label {
    color: #94A3B8;
    font-size: 0.82rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 0.3rem;
}

/* ---- Section title ---- */
.section-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: #C4B5FD;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin: 2rem 0 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.section-title::after {
    content: "";
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, rgba(124,58,237,0.4), transparent);
    margin-left: 0.5rem;
}

/* ---- Tool cards ---- */
.tool-card {
    background: linear-gradient(135deg, rgba(26,26,46,0.95), rgba(22,33,62,0.9));
    border: 1px solid rgba(124,58,237,0.22);
    border-radius: 18px;
    padding: 1.6rem 1.2rem;
    text-align: center;
    transition: all 0.3s ease;
    cursor: pointer;
    min-height: 140px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    backdrop-filter: blur(8px);
}
.tool-card:hover {
    border-color: rgba(124,58,237,0.75);
    transform: translateY(-6px);
    box-shadow: 0 16px 40px rgba(124,58,237,0.25);
    background: linear-gradient(135deg, rgba(36,36,60,0.98), rgba(30,43,72,0.95));
}
.tool-icon { font-size: 2.6rem; margin-bottom: 0.6rem; }
.tool-name { font-size: 1rem; font-weight: 700; color: #C4B5FD; margin-bottom: 0.3rem; }
.tool-desc { font-size: 0.78rem; color: #64748B; line-height: 1.4; }

/* ---- Welcome banner ---- */
.welcome-banner {
    background: linear-gradient(135deg, rgba(124,58,237,0.15) 0%, rgba(236,72,153,0.1) 50%, rgba(245,158,11,0.08) 100%);
    border: 1px solid rgba(124,58,237,0.3);
    border-radius: 20px;
    padding: 1.75rem 2rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}
.welcome-banner::after {
    content: "⚡";
    position: absolute;
    right: 2rem;
    top: 50%;
    transform: translateY(-50%);
    font-size: 5rem;
    opacity: 0.07;
}

/* ---- Metric tweaks ---- */
[data-testid="stMetric"] {
    background: linear-gradient(135deg, rgba(26,26,46,0.9), rgba(22,33,62,0.85));
    border: 1px solid rgba(124,58,237,0.3);
    border-radius: 14px;
    padding: 1rem 1.2rem;
}
[data-testid="stMetricValue"] { color: #A78BFA !important; font-weight: 800 !important; }
[data-testid="stMetricLabel"] { color: #94A3B8 !important; font-size: 0.8rem !important; text-transform: uppercase; letter-spacing: 0.06em; }
</style>
""", unsafe_allow_html=True)

# ── Welcome Banner ────────────────────────────────────────────────────────────
name = st.session_state.get("full_name") or st.session_state.get("email", "User")
first_name = name.split()[0] if name else "User"
tier = st.session_state.get("tier", "free")
tier_badge = "⭐ Pro" if tier == "pro" else "🆓 Free"
tier_color = "#F59E0B" if tier == "pro" else "#7C3AED"

st.markdown(f"""
<div class="welcome-banner">
    <div style="display:flex; align-items:center; gap:1rem; flex-wrap:wrap;">
        <div>
            <h1 style="font-size:1.9rem; font-weight:900; margin:0; line-height:1.1;">
                👋 Welcome back, <span class="gradient-text">{first_name}</span>
            </h1>
            <p style="color:#94A3B8; margin:0.4rem 0 0; font-size:0.95rem;">
                Your AI workspace is ready · <span style="color:{tier_color}; font-weight:700;">{tier_badge}</span>
            </p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Usage Stats ───────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">📊 Usage Overview</div>', unsafe_allow_html=True)

try:
    stats = api_stats()
    total_req = stats.get("total_requests", 0)
    total_tok = stats.get("total_tokens_used", 0)
    breakdown = stats.get("feature_breakdown", {})
    top_feature = max(breakdown, key=breakdown.get) if breakdown else "—"
    icon_map = {"chat":"💬","summarize":"📝","translate":"🌍","code":"💻","grammar":"✅","email":"📧","resume":"📄","prompt":"🎯"}
    top_icon = icon_map.get(top_feature, "🔥")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
        <div class="stat-card">
            <span class="stat-icon">📊</span>
            <div class="stat-value">{total_req}</div>
            <div class="stat-label">Total Requests</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        tok_display = f"{total_tok:,}" if total_tok < 1_000_000 else f"{total_tok/1_000_000:.1f}M"
        st.markdown(f"""
        <div class="stat-card">
            <span class="stat-icon">⚡</span>
            <div class="stat-value" style="font-size:2.2rem;">{tok_display}</div>
            <div class="stat-label">Tokens Used</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="stat-card">
            <span class="stat-icon">{top_icon}</span>
            <div class="stat-value" style="font-size:1.3rem;">{top_feature.title()}</div>
            <div class="stat-label">Top Tool</div>
        </div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
        <div class="stat-card">
            <span class="stat-icon">{tier_badge.split()[0]}</span>
            <div class="stat-value" style="font-size:1.3rem; color:{tier_color}; -webkit-text-fill-color:{tier_color};">{tier.title()}</div>
            <div class="stat-label">Current Plan</div>
        </div>""", unsafe_allow_html=True)

    # ── Feature Breakdown ─────────────────────────────────────────────────────
    if breakdown:
        st.markdown('<div class="section-title" style="margin-top:1.5rem;">🔥 Feature Breakdown</div>', unsafe_allow_html=True)
        total_b = sum(breakdown.values()) or 1
        cols_b = st.columns(len(breakdown))
        for col, (feat, count) in zip(cols_b, sorted(breakdown.items(), key=lambda x: -x[1])):
            pct = int(count / total_b * 100)
            col.metric(f"{icon_map.get(feat,'🤖')} {feat.title()}", count, f"{pct}%")

except ValueError as e:
    st.info(f"📊 Stats unavailable: {e}")

st.markdown("<br>", unsafe_allow_html=True)

# ── Tool Grid ─────────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">🚀 Quick Access</div>', unsafe_allow_html=True)

tools = [
    ("💬", "Chatbot",          "Chat with a powerful AI",         "pages/1_Chatbot.py"),
    ("📝", "Summarizer",       "Condense long text instantly",     "pages/2_Summarizer.py"),
    ("🌍", "Translator",       "Translate to 100+ languages",      "pages/3_Translator.py"),
    ("💻", "Code Generator",   "Generate & explain code",          "pages/4_Code_Generator.py"),
    ("✅", "Grammar Checker",  "Polish your writing",              "pages/5_Grammar.py"),
    ("📧", "Email Writer",     "Draft professional emails",        "pages/6_Email_Writer.py"),
    ("📄", "Resume Builder",   "Create ATS-friendly resumes",      "pages/7_Resume.py"),
    ("🎯", "Prompt Generator", "Engineer perfect AI prompts",      "pages/8_Prompt_Generator.py"),
    ("🕐", "History",          "Review past interactions",         "pages/9_History.py"),
]

rows = [tools[:3], tools[3:6], tools[6:]]
for row in rows:
    cols = st.columns(3)
    for col, (icon, name_, desc, path) in zip(cols, row):
        with col:
            st.markdown(f"""
            <div class="tool-card">
                <div class="tool-icon">{icon}</div>
                <div class="tool-name">{name_}</div>
                <div class="tool-desc">{desc}</div>
            </div>""", unsafe_allow_html=True)
            if st.button(f"Open {name_}", key=f"dash_open_{name_}", use_container_width=True):
                st.switch_page(path)
    st.markdown("<br>", unsafe_allow_html=True)
