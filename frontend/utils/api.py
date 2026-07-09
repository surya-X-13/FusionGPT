"""
Shared API client utilities for the FusionGPT Streamlit frontend.
All pages import from this module to call the FastAPI backend.
"""
import os
from pathlib import Path
import requests
import streamlit as st
from typing import Optional

BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000/api/v1")


# ---------------------------------------------------------------------------
# Auth helpers
# ---------------------------------------------------------------------------
def get_token() -> Optional[str]:
    return st.session_state.get("token")


def get_headers() -> dict:
    token = get_token()
    if not token:
        return {}
    return {"Authorization": f"Bearer {token}"}


def is_authenticated() -> bool:
    return bool(get_token())


def logout():
    for key in ["token", "user_id", "email", "full_name", "tier"]:
        st.session_state.pop(key, None)
    st.rerun()


# ---------------------------------------------------------------------------
# Auth API calls
# ---------------------------------------------------------------------------
def api_register(email: str, password: str, full_name: str) -> dict:
    resp = requests.post(
        f"{BASE_URL}/auth/register",
        json={"email": email, "password": password, "full_name": full_name},
        timeout=60,
    )
    return _handle(resp)


def api_login(email: str, password: str) -> dict:
    resp = requests.post(
        f"{BASE_URL}/auth/login",
        json={"email": email, "password": password},
        timeout=60,
    )
    return _handle(resp)


def save_session(data: dict):
    """Store token and user info in session_state after login/register."""
    st.session_state["token"] = data["access_token"]
    st.session_state["user_id"] = data["user_id"]
    st.session_state["email"] = data["email"]
    st.session_state["full_name"] = data.get("full_name", "")
    st.session_state["tier"] = data.get("tier", "free")


# ---------------------------------------------------------------------------
# AI Tool API calls
# ---------------------------------------------------------------------------
def api_chat(message: str, history: list) -> dict:
    resp = requests.post(
        f"{BASE_URL}/chat/",
        json={"message": message, "history": history},
        headers=get_headers(),
        timeout=60,
    )
    return _handle(resp)


def api_summarize(text: str, length: str = "medium") -> dict:
    resp = requests.post(
        f"{BASE_URL}/summarize/",
        json={"text": text, "length": length},
        headers=get_headers(),
        timeout=60,
    )
    return _handle(resp)


def api_translate(text: str, target_language: str, source_language: str = "auto") -> dict:
    resp = requests.post(
        f"{BASE_URL}/translate/",
        json={"text": text, "target_language": target_language, "source_language": source_language},
        headers=get_headers(),
        timeout=60,
    )
    return _handle(resp)


def api_code(description: str, language: str, task: str = "generate", code_to_explain: str = None) -> dict:
    payload = {"description": description, "language": language, "task": task}
    if code_to_explain:
        payload["code_to_explain"] = code_to_explain
    resp = requests.post(
        f"{BASE_URL}/code/",
        json=payload,
        headers=get_headers(),
        timeout=60,
    )
    return _handle(resp)


def api_grammar(text: str) -> dict:
    resp = requests.post(
        f"{BASE_URL}/grammar/",
        json={"text": text},
        headers=get_headers(),
        timeout=60,
    )
    return _handle(resp)


def api_email(context: str, recipient: str, tone: str, additional_info: str = None) -> dict:
    resp = requests.post(
        f"{BASE_URL}/email/",
        json={"context": context, "recipient": recipient, "tone": tone, "additional_info": additional_info},
        headers=get_headers(),
        timeout=60,
    )
    return _handle(resp)


def api_resume(job_title: str, years_experience: int, key_skills: str, recent_role: str = "", achievements: str = None) -> dict:
    resp = requests.post(
        f"{BASE_URL}/resume/",
        json={
            "job_title": job_title,
            "years_experience": years_experience,
            "key_skills": key_skills,
            "recent_role": recent_role,
            "achievements": achievements,
        },
        headers=get_headers(),
        timeout=60,
    )
    return _handle(resp)


def api_prompt(goal: str, context: str = None, output_format: str = None) -> dict:
    resp = requests.post(
        f"{BASE_URL}/prompt/",
        json={"goal": goal, "context": context, "output_format": output_format},
        headers=get_headers(),
        timeout=60,
    )
    return _handle(resp)


def api_history(limit: int = 50, feature: str = None) -> list:
    params = {"limit": limit}
    if feature:
        params["feature"] = feature
    resp = requests.get(
        f"{BASE_URL}/history/",
        params=params,
        headers=get_headers(),
        timeout=15,
    )
    return _handle(resp)


def api_stats() -> dict:
    resp = requests.get(
        f"{BASE_URL}/history/stats",
        headers=get_headers(),
        timeout=15,
    )
    return _handle(resp)


# ---------------------------------------------------------------------------
# Internal: response handler
# ---------------------------------------------------------------------------
def _handle(resp: requests.Response):
    try:
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.HTTPError as e:
        try:
            detail = resp.json().get("detail", str(e))
        except Exception:
            detail = str(e)
        raise ValueError(detail)
    except requests.exceptions.ConnectionError:
        raise ValueError("Cannot connect to backend. Make sure the API server is running on port 8000.")
    except requests.exceptions.Timeout:
        raise ValueError("Request timed out. The AI is thinking too long — please try again.")


# ---------------------------------------------------------------------------
# UI helpers shared across pages
# ---------------------------------------------------------------------------
GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

*, *::before, *::after { box-sizing: border-box; }
* { font-family: 'Inter', sans-serif !important; }

/* ── App background ── */
.stApp {
    background: linear-gradient(135deg, #080810 0%, #0e0e1c 40%, #080810 100%) !important;
    color: #E2E8F0 !important;
}
.main { background: transparent !important; }

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }

/* ── Block container ── */
.main .block-container {
    padding-top: 1.5rem;
    padding-bottom: 3rem;
    max-width: 1100px;
}

/* ── Gradient text ── */
.gradient-text {
    background: linear-gradient(135deg, #A78BFA 0%, #EC4899 55%, #F59E0B 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-weight: 900;
}

/* ── Premium buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #7C3AED 0%, #6D28D9 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.03em !important;
    padding: 0.6rem 1.4rem !important;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 0 4px 20px rgba(124, 58, 237, 0.4) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(124, 58, 237, 0.55) !important;
    background: linear-gradient(135deg, #8B5CF6 0%, #7C3AED 100%) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #08081a 0%, #0f0f26 50%, #0a0a18 100%) !important;
    border-right: 1px solid rgba(124, 58, 237, 0.25) !important;
    box-shadow: 4px 0 30px rgba(0,0,0,0.4) !important;
}
section[data-testid="stSidebar"] > div { background: transparent !important; }

/* ── Sidebar nav links ── */
[data-testid="stSidebarNav"] a {
    border-radius: 10px !important;
    padding: 0.5rem 0.75rem !important;
    color: #CBD5E1 !important;
    font-weight: 500 !important;
    transition: all 0.2s ease !important;
}
[data-testid="stSidebarNav"] a:hover {
    background: rgba(124,58,237,0.15) !important;
    color: #A78BFA !important;
}
[data-testid="stSidebarNav"] a[aria-selected="true"] {
    background: rgba(124,58,237,0.25) !important;
    color: #C4B5FD !important;
    font-weight: 700 !important;
    border-left: 3px solid #7C3AED !important;
}

/* ── Inputs ── */
.stTextArea textarea, .stTextInput input {
    background: rgba(15, 15, 30, 0.95) !important;
    border: 1px solid rgba(124, 58, 237, 0.35) !important;
    border-radius: 12px !important;
    color: #E2E8F0 !important;
    font-size: 0.95rem !important;
    transition: all 0.2s ease !important;
    caret-color: #A78BFA !important;
}
.stTextArea textarea:focus, .stTextInput input:focus {
    border-color: #7C3AED !important;
    box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.18) !important;
}
.stTextArea textarea::placeholder, .stTextInput input::placeholder { color: #475569 !important; }

/* ── Select boxes ── */
.stSelectbox > div > div {
    background: rgba(15, 15, 30, 0.95) !important;
    border: 1px solid rgba(124, 58, 237, 0.35) !important;
    border-radius: 12px !important;
    color: #E2E8F0 !important;
}
.stSelectbox svg { fill: #7C3AED !important; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(15,15,30,0.6) !important;
    border-radius: 12px !important;
    padding: 4px !important;
    gap: 4px !important;
    border: 1px solid rgba(124,58,237,0.2) !important;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 9px !important;
    color: #94A3B8 !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    padding: 0.45rem 1.2rem !important;
    transition: all 0.2s ease !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #7C3AED, #6D28D9) !important;
    color: white !important;
    box-shadow: 0 4px 12px rgba(124,58,237,0.4) !important;
}
.stTabs [data-baseweb="tab-highlight"] { display: none !important; }

/* ── Cards ── */
.ai-card {
    background: linear-gradient(135deg, rgba(26,26,46,0.95) 0%, rgba(22,33,62,0.9) 100%);
    border: 1px solid rgba(124, 58, 237, 0.3);
    border-radius: 18px;
    padding: 1.5rem;
    margin: 0.75rem 0;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3), 0 0 0 1px rgba(124,58,237,0.08);
    backdrop-filter: blur(10px);
    transition: all 0.3s ease;
}
.ai-card:hover {
    border-color: rgba(124,58,237,0.5);
    box-shadow: 0 12px 40px rgba(124,58,237,0.18);
}

/* ── Output box ── */
.output-box {
    background: linear-gradient(135deg, rgba(124,58,237,0.06), rgba(236,72,153,0.04));
    border: 1px solid rgba(124, 58, 237, 0.35);
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    margin-top: 0.75rem;
    line-height: 1.8;
    color: #CBD5E1;
    font-size: 0.95rem;
    position: relative;
}
.output-box::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #7C3AED, #EC4899, transparent);
    border-radius: 14px 14px 0 0;
}

/* ── Token badge ── */
.token-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    background: rgba(124, 58, 237, 0.18);
    border: 1px solid rgba(124, 58, 237, 0.4);
    color: #C4B5FD;
    font-size: 0.78rem;
    font-weight: 700;
    padding: 0.25rem 0.9rem;
    border-radius: 999px;
    margin-top: 0.6rem;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}

/* ── Page header ── */
.page-header {
    padding: 1.25rem 0 1.25rem;
    margin-bottom: 1.75rem;
    border-bottom: 1px solid rgba(124, 58, 237, 0.2);
    position: relative;
}
.page-header::after {
    content: "";
    position: absolute;
    bottom: -1px; left: 0;
    width: 80px; height: 2px;
    background: linear-gradient(90deg, #7C3AED, #EC4899);
    border-radius: 2px;
}

/* ── Divider ── */
hr {
    border: none !important;
    border-top: 1px solid rgba(124, 58, 237, 0.2) !important;
    margin: 1.5rem 0 !important;
}

/* ── Metrics ── */
[data-testid="stMetric"] {
    background: linear-gradient(135deg, rgba(26,26,46,0.9), rgba(22,33,62,0.85)) !important;
    border: 1px solid rgba(124,58,237,0.3) !important;
    border-radius: 14px !important;
    padding: 1rem 1.25rem !important;
    transition: all 0.25s ease !important;
}
[data-testid="stMetric"]:hover {
    border-color: rgba(124,58,237,0.55) !important;
    transform: translateY(-2px) !important;
}
[data-testid="stMetricValue"] { color: #A78BFA !important; font-weight: 900 !important; }
[data-testid="stMetricLabel"] {
    color: #94A3B8 !important;
    font-size: 0.78rem !important;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}

/* ── Expander ── */
.streamlit-expanderHeader {
    background: rgba(26,26,46,0.8) !important;
    border-radius: 12px !important;
    border: 1px solid rgba(124,58,237,0.25) !important;
    color: #CBD5E1 !important;
    font-weight: 600 !important;
}
.streamlit-expanderContent {
    background: rgba(15,15,30,0.5) !important;
    border: 1px solid rgba(124,58,237,0.15) !important;
    border-top: none !important;
    border-radius: 0 0 12px 12px !important;
}

/* ── Chat bubbles ── */
.chat-user {
    background: linear-gradient(135deg, #7C3AED, #6D28D9);
    border-radius: 20px 20px 4px 20px;
    padding: 0.85rem 1.25rem;
    margin: 0.5rem 0 0.5rem auto;
    max-width: 75%;
    color: white;
    font-size: 0.95rem;
    box-shadow: 0 4px 15px rgba(124,58,237,0.35);
}
.chat-ai {
    background: linear-gradient(135deg, rgba(26,26,46,0.9), rgba(22,33,62,0.85));
    border: 1px solid rgba(124, 58, 237, 0.3);
    border-radius: 20px 20px 20px 4px;
    padding: 0.85rem 1.25rem;
    margin: 0.5rem auto 0.5rem 0;
    max-width: 85%;
    color: #E2E8F0;
    font-size: 0.95rem;
    line-height: 1.65;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: rgba(15,15,30,0.5); }
::-webkit-scrollbar-thumb { background: rgba(124,58,237,0.5); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: rgba(124,58,237,0.75); }
</style>
"""


def get_asset_path(relative_path: str) -> str:
    """Resolve asset paths from either the frontend directory or repo root."""
    candidates = [
        Path(__file__).resolve().parents[1] / relative_path,
        Path(__file__).resolve().parents[2] / relative_path,
    ]
    for candidate in candidates:
        if candidate.exists():
            return str(candidate)
    return str(candidates[0])


def get_logo_path() -> str:
    """Resolve the brand logo from the assets folder."""
    logo = Path(__file__).resolve().parents[1] / "assets" / "logo.png"
    return str(logo)


def inject_global_css():
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)


def page_header(icon: str, title: str, subtitle: str = ""):
    st.markdown(
        f"""
        <div class="page-header">
            <h1 style="font-size:2rem; font-weight:900; margin:0; line-height:1.1;">
                {icon} <span class="gradient-text">{title}</span>
            </h1>
            {'<p style="color:#94A3B8; margin:0.5rem 0 0; font-size:0.95rem;">' + subtitle + '</p>' if subtitle else ''}
        </div>
        """,
        unsafe_allow_html=True,
    )


def require_auth():
    """Redirect to Home if not authenticated."""
    if not is_authenticated():
        st.markdown("""
        <div style="text-align:center; padding:3rem 1rem;">
            <div style="font-size:3rem; margin-bottom:1rem;">🔐</div>
            <h2 style="color:#A78BFA; margin:0 0 0.5rem;">Authentication Required</h2>
            <p style="color:#64748B; margin:0 0 1.5rem;">Please log in to access this feature.</p>
        </div>
        """, unsafe_allow_html=True)
        st.page_link("Home.py", label="🔐 Go to Login", icon="🔑")
        st.stop()


def render_sidebar_user():
    """Render user info + logout in the sidebar."""
    with st.sidebar:
        # ── Brand header ──
        logo_path = get_logo_path()
        col_logo_sb, col_title_sb = st.columns([1, 2])
        with col_logo_sb:
            st.image(logo_path, use_container_width=True)
        with col_title_sb:
            st.markdown(
                '<h2 style="font-size:1.3rem; font-weight:900; margin:0; line-height:2.3;'
                'background:linear-gradient(135deg,#A78BFA,#EC4899);-webkit-background-clip:text;'
                '-webkit-text-fill-color:transparent;background-clip:text;">FusionGPT</h2>',
                unsafe_allow_html=True,
            )
        st.markdown("<hr style='margin: 0.5rem 0 1rem; border-color: rgba(124,58,237,0.2);'>", unsafe_allow_html=True)

        if is_authenticated():
            name = st.session_state.get("full_name") or st.session_state.get("email", "User")
            tier = st.session_state.get("tier", "free")
            tier_color = "#F59E0B" if tier == "pro" else "#7C3AED"
            tier_icon = "⭐" if tier == "pro" else "🆓"
            st.markdown(
                f"""
                <div style="padding:0.9rem 1rem; background:rgba(124,58,237,0.1); border-radius:14px;
                            border:1px solid rgba(124,58,237,0.3); margin-bottom:1rem;">
                    <p style="margin:0; font-weight:700; font-size:0.95rem; color:#E2E8F0;">👤 {name}</p>
                    <span style="font-size:0.72rem; color:{tier_color}; font-weight:700;
                                 text-transform:uppercase; letter-spacing:0.07em;">
                        {tier_icon} {tier} plan
                    </span>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button("🚪 Logout", use_container_width=True, key="sidebar_logout_btn"):
                logout()
