"""
FusionGPT — Home Page (Login / Register)
Entry point: streamlit run Home.py
"""
import base64
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st
import streamlit.components.v1 as components
from utils.api import (
    inject_global_css,
    is_authenticated,
    api_login,
    api_register,
    save_session,
    get_logo_path,
)

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FusionGPT — AI-Powered Tools",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_global_css()

# ── Auth card extra styles ────────────────────────────────────────────────────
st.markdown("""
<style>
.auth-wrapper {
    max-width: 460px;
    margin: 0 auto;
}
.auth-card-inner {
    background: linear-gradient(135deg, rgba(18,18,38,0.98), rgba(14,14,30,0.95));
    border: 1px solid rgba(124,58,237,0.35);
    border-radius: 24px;
    padding: 2rem 2.25rem;
    box-shadow: 0 24px 70px rgba(0,0,0,0.5), 0 0 0 1px rgba(124,58,237,0.1);
    backdrop-filter: blur(20px);
}
</style>
""", unsafe_allow_html=True)

# ── Redirect if already logged in ─────────────────────────────────────────────
if is_authenticated():
    st.switch_page("pages/0_Dashboard.py")

# ── Hero section (full inline HTML for rich animations) ───────────────────────
def render_hero():
    logo_path = get_logo_path()
    try:
        with open(logo_path, "rb") as f:
            logo_b64 = base64.b64encode(f.read()).decode()
        logo_src = f"data:image/png;base64,{logo_b64}"
    except Exception:
        logo_src = ""

    html = f"""
    <style>
        :root {{ color-scheme: dark; }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ font-family: Inter, -apple-system, sans-serif; background: transparent; }}

        .hero {{
            position: relative;
            overflow: hidden;
            border-radius: 28px;
            padding: 2.5rem 2rem;
            background: linear-gradient(135deg, rgba(12,12,24,0.97) 0%, rgba(18,18,40,0.95) 100%);
            border: 1px solid rgba(124,58,237,0.3);
            box-shadow: 0 30px 80px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.05);
        }}

        /* animated blobs */
        .blob {{
            position: absolute;
            border-radius: 999px;
            filter: blur(80px);
            opacity: 0.3;
            pointer-events: none;
            animation: blobFloat 8s ease-in-out infinite alternate;
        }}
        .blob-1 {{ width:300px; height:300px; background:#7C3AED; top:-80px; right:-60px; animation-duration:9s; }}
        .blob-2 {{ width:220px; height:220px; background:#EC4899; bottom:-80px; left:-50px; animation-duration:11s; }}
        .blob-3 {{ width:180px; height:180px; background:#F59E0B; top:30%; left:35%; opacity:0.12; animation-duration:13s; }}
        @keyframes blobFloat {{
            from {{ transform: translate3d(0,0,0) scale(1); }}
            to   {{ transform: translate3d(20px,-20px,0) scale(1.08); }}
        }}

        /* Floating dots */
        .dot {{
            position: absolute;
            border-radius: 999px;
            animation: dotPulse 4s ease-in-out infinite;
        }}
        @keyframes dotPulse {{
            0%, 100% {{ opacity: 0.6; transform: scale(1); }}
            50%  {{ opacity: 1;   transform: scale(1.4); box-shadow: 0 0 20px currentColor; }}
        }}

        /* Layout */
        .hero-grid {{
            display: grid;
            grid-template-columns: 1.1fr 0.9fr;
            gap: 2rem;
            align-items: center;
            position: relative;
            z-index: 1;
        }}

        /* Copy side */
        .hero-eyebrow {{
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            background: rgba(124,58,237,0.15);
            border: 1px solid rgba(124,58,237,0.35);
            color: #C4B5FD;
            font-size: 0.78rem;
            font-weight: 700;
            padding: 0.35rem 0.9rem;
            border-radius: 999px;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            margin-bottom: 1rem;
        }}
        .hero-title {{
            font-size: clamp(1.9rem, 3.4vw, 3rem);
            font-weight: 900;
            line-height: 1.08;
            margin-bottom: 1rem;
            background: linear-gradient(135deg, #C4B5FD 0%, #F9A8D4 40%, #FCD34D 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .hero-sub {{
            color: #94A3B8;
            line-height: 1.75;
            font-size: 1rem;
            margin-bottom: 1.5rem;
        }}
        .badge-row {{
            display: flex;
            gap: 0.6rem;
            flex-wrap: wrap;
        }}
        .badge {{
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
            border: 1px solid rgba(124,58,237,0.3);
            background: rgba(124,58,237,0.1);
            color: #DDD6FE;
            padding: 0.4rem 0.8rem;
            border-radius: 999px;
            font-size: 0.82rem;
            font-weight: 600;
            backdrop-filter: blur(6px);
        }}

        /* Panel side */
        .hero-panel {{
            border-radius: 22px;
            padding: 1.5rem;
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.07);
            backdrop-filter: blur(16px);
        }}
        .logo-wrap {{
            display: flex;
            justify-content: center;
            margin-bottom: 1.25rem;
        }}
        .logo-wrap img {{
            width: 140px;
            border-radius: 20px;
            box-shadow: 0 16px 40px rgba(124,58,237,0.3), 0 0 0 1px rgba(124,58,237,0.15);
            transition: transform 0.4s ease;
        }}
        .logo-wrap img:hover {{ transform: scale(1.05) rotate(-1deg); }}

        .feat-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 0.6rem;
        }}
        .feat {{
            border-radius: 14px;
            padding: 0.75rem 0.6rem;
            background: rgba(124,58,237,0.1);
            border: 1px solid rgba(124,58,237,0.18);
            text-align: center;
            color: #EDE9FE;
            font-size: 0.88rem;
            font-weight: 600;
            transition: all 0.25s ease;
        }}
        .feat:hover {{
            background: rgba(124,58,237,0.2);
            border-color: rgba(124,58,237,0.45);
            transform: translateY(-2px);
        }}

        @media (max-width: 860px) {{
            .hero-grid {{ grid-template-columns: 1fr; }}
            .hero-panel {{ display: none; }}
        }}
    </style>

    <div class="hero">
        <div class="blob blob-1"></div>
        <div class="blob blob-2"></div>
        <div class="blob blob-3"></div>
        <div class="dot" style="width:8px;height:8px;background:#F59E0B;top:15%;left:10%;"></div>
        <div class="dot" style="width:6px;height:6px;background:#EC4899;bottom:20%;right:12%;animation-delay:1.5s;"></div>
        <div class="dot" style="width:5px;height:5px;background:#7C3AED;top:60%;left:20%;animation-delay:3s;"></div>

        <div class="hero-grid">
            <div class="hero-copy">
                <div class="hero-eyebrow">🤖 Powered by Groq · llama-3.3-70b</div>
                <h1 class="hero-title">Your AI Toolkit,<br>Supercharged ⚡</h1>
                <p class="hero-sub">
                    8 powerful AI tools in one sleek platform — chat, summarize,
                    translate, write code, fix grammar, draft emails, build resumes,
                    and engineer prompts. Blazing-fast Groq inference.
                </p>
                <div class="badge-row">
                    <div class="badge">⚡ Instant Responses</div>
                    <div class="badge">🧠 8 AI Tools</div>
                    <div class="badge">🔐 Secure Auth</div>
                    <div class="badge">📊 Usage Analytics</div>
                </div>
            </div>
            <div class="hero-panel">
                <div class="logo-wrap">
                    {"<img src='" + logo_src + "' alt='FusionGPT'/>" if logo_src else "<div style='font-size:4rem;text-align:center'>🤖</div>"}
                </div>
                <div class="feat-grid">
                    <div class="feat">💬 Chat</div>
                    <div class="feat">📝 Summarize</div>
                    <div class="feat">🌍 Translate</div>
                    <div class="feat">💻 Code</div>
                    <div class="feat">✅ Grammar</div>
                    <div class="feat">📧 Email</div>
                    <div class="feat">📄 Resume</div>
                    <div class="feat">🎯 Prompts</div>
                </div>
            </div>
        </div>
    </div>
    """
    components.html(html, height=500, scrolling=False)


render_hero()
st.markdown("<br>", unsafe_allow_html=True)

# ── Auth Form ─────────────────────────────────────────────────────────────────
left_sp, auth_col, right_sp = st.columns([1, 1.6, 1])
with auth_col:
    st.markdown('<div class="auth-card-inner">', unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align:center; margin-bottom:1.5rem;">
        <h2 style="font-size:1.5rem; font-weight:900; margin:0 0 0.3rem;">
            🔐 <span style="background:linear-gradient(135deg,#A78BFA,#EC4899);
            -webkit-background-clip:text;-webkit-text-fill-color:transparent;">Get Started</span>
        </h2>
        <p style="color:#64748B; font-size:0.85rem; margin:0;">Create an account or sign in to continue</p>
    </div>
    """, unsafe_allow_html=True)

    tab_login, tab_register = st.tabs(["  Sign In  ", "  Create Account  "])

    # ---------- Login ----------
    with tab_login:
        with st.form("login_form"):
            email = st.text_input("Email", placeholder="you@example.com", key="login_email")
            password = st.text_input("Password", type="password", placeholder="••••••••", key="login_pw")
            submitted = st.form_submit_button("Sign In →", use_container_width=True)

        if submitted:
            if not email or not password:
                st.error("Please fill in all fields.")
            else:
                with st.spinner("Authenticating..."):
                    try:
                        data = api_login(email, password)
                        save_session(data)
                        st.success(f"Welcome back, {data.get('full_name') or data['email']}! 🎉")
                        st.switch_page("pages/0_Dashboard.py")
                    except ValueError as e:
                        st.error(f"❌ {e}")

    # ---------- Register ----------
    with tab_register:
        with st.form("register_form"):
            full_name = st.text_input("Full Name", placeholder="Jane Doe", key="reg_name")
            reg_email = st.text_input("Email", placeholder="you@example.com", key="reg_email")
            reg_pw = st.text_input("Password", type="password", placeholder="Min. 6 characters", key="reg_pw")
            submitted_reg = st.form_submit_button("Create Account →", use_container_width=True)

        if submitted_reg:
            if not reg_email or not reg_pw:
                st.error("Email and password are required.")
            elif len(reg_pw) < 6:
                st.error("Password must be at least 6 characters.")
            else:
                with st.spinner("Creating your account..."):
                    try:
                        data = api_register(reg_email, reg_pw, full_name)
                        save_session(data)
                        st.success("Account created! Welcome to FusionGPT 🚀")
                        st.switch_page("pages/0_Dashboard.py")
                    except ValueError as e:
                        st.error(f"❌ {e}")

    st.markdown('</div>', unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<br>
<div style="text-align:center; color:#334155; font-size:0.78rem; margin-top:2rem; padding-bottom:1rem;">
    ⚡ Powered by <span style="color:#7C3AED;">Groq</span> ·
    llama-3.3-70b-versatile ·
    Built with <span style="color:#EC4899;">FastAPI</span> &amp;
    <span style="color:#A78BFA;">Streamlit</span>
</div>
""", unsafe_allow_html=True)
