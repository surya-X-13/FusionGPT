from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database.database import engine, Base
from api import auth, chat, summarize, translate, code, grammar, email, resume, prompt, history

# ---------------------------------------------------------------------------
# Create all DB tables on startup
# ---------------------------------------------------------------------------
Base.metadata.create_all(bind=engine)

# ---------------------------------------------------------------------------
# FastAPI application
# ---------------------------------------------------------------------------
app = FastAPI(
    title="FusionGPT API",
    description=(
        "A multi-tool AI SaaS platform powered by Groq (llama-3.3-70b-versatile). "
        "Features: Chat, Summarization, Translation, Code Generation, Grammar Check, "
        "Email Writer, Resume Builder, and Prompt Generator."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ---------------------------------------------------------------------------
# CORS — allow Streamlit frontend (localhost:8501) and any local dev origins
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8501",
        "http://127.0.0.1:8501",
        "http://localhost:3000",
        "*",   # Loosen for local dev; tighten in production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Register all routers under /api/v1
# ---------------------------------------------------------------------------
API_PREFIX = "/api/v1"

app.include_router(auth.router,      prefix=API_PREFIX)
app.include_router(chat.router,      prefix=API_PREFIX)
app.include_router(summarize.router, prefix=API_PREFIX)
app.include_router(translate.router, prefix=API_PREFIX)
app.include_router(code.router,      prefix=API_PREFIX)
app.include_router(grammar.router,   prefix=API_PREFIX)
app.include_router(email.router,     prefix=API_PREFIX)
app.include_router(resume.router,    prefix=API_PREFIX)
app.include_router(prompt.router,    prefix=API_PREFIX)
app.include_router(history.router,   prefix=API_PREFIX)


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------
@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "message": "FusionGPT API is running 🚀"}


@app.get("/health", tags=["Health"])
def health():
    return {"status": "healthy"}
