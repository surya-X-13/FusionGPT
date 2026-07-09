# MiniAI-SaaS 🤖

A full-stack AI SaaS platform with **8 AI-powered tools** in one interface — built with FastAPI, Groq, and Streamlit.

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green)
![Streamlit](https://img.shields.io/badge/Streamlit-1.40-red)
![Groq](https://img.shields.io/badge/LLM-Groq%20llama--3.3--70b-purple)

---

## ✨ Features

| Tool | Description |
|------|-------------|
| 💬 **AI Chatbot** | Conversational assistant with full history support |
| 📝 **Summarizer** | Condense any text — short, medium, or long |
| 🌍 **Translator** | 50+ languages with auto-detect source |
| 💻 **Code Generator** | Generate or explain code in 24+ languages |
| ✅ **Grammar Checker** | Fix grammar, spelling, and style |
| 📧 **Email Writer** | Draft emails with 5 tone options |
| 📄 **Resume Builder** | ATS-friendly resume content generator |
| 🎯 **Prompt Generator** | Engineer perfect AI prompts |

Plus: 📊 **Dashboard** with usage stats and 🕐 **History** with full interaction log.

---

## 🏗️ Architecture

```
MiniAI-SaaS/
├── backend/         # FastAPI REST API
│   ├── api/         # Route handlers (one file per feature)
│   ├── services/    # LLM (Groq) + system prompt templates
│   ├── database/    # SQLAlchemy ORM (SQLite default)
│   ├── schemas/     # Pydantic v2 request/response models
│   ├── utils/       # JWT auth helpers
│   └── main.py      # App entry point
│
└── frontend/        # Streamlit multi-page app
    ├── Home.py      # Landing page (login/register)
    ├── Dashboard.py # Usage dashboard
    └── pages/       # 9 AI tool pages
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- A [Groq API key](https://console.groq.com/keys) (free tier available)

### 1. Backend Setup

```bash
cd backend
pip install -r requirements.txt
```

Edit `.env` and add your keys:
```env
GROQ_API_KEY=your_groq_api_key_here
SECRET_KEY=your_random_jwt_secret_here
DATABASE_URL=sqlite:///./miniAI.db
```

Start the API server:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Frontend Setup

```bash
cd frontend
pip install -r requirements.txt
streamlit run Home.py
```

Open **http://localhost:8501** in your browser.

---

## 📡 API Reference

Base URL: `http://localhost:8000/api/v1`

Interactive docs: `http://localhost:8000/docs`

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Create account |
| POST | `/auth/login` | Get JWT token |
| GET | `/auth/me` | Get profile |
| POST | `/chat/` | AI chat |
| POST | `/summarize/` | Summarize text |
| POST | `/translate/` | Translate text |
| POST | `/code/` | Generate/explain code |
| POST | `/grammar/` | Check grammar |
| POST | `/email/` | Draft email |
| POST | `/resume/` | Build resume content |
| POST | `/prompt/` | Generate AI prompt |
| GET | `/history/` | Get usage history |
| GET | `/history/stats` | Get usage statistics |

All AI endpoints require `Authorization: Bearer <token>` header.

---

## ⚙️ Environment Variables

### Backend (`backend/.env`)
| Variable | Required | Description |
|----------|----------|-------------|
| `GROQ_API_KEY` | ✅ | Your Groq API key |
| `SECRET_KEY` | ✅ | JWT signing secret (use a strong random string) |
| `DATABASE_URL` | Optional | DB URL (default: SQLite) |

---

## 🔧 Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | FastAPI + Uvicorn |
| LLM Provider | Groq (`llama-3.3-70b-versatile`) |
| Database | SQLAlchemy + SQLite |
| Auth | JWT (python-jose) + bcrypt |
| Frontend | Streamlit (multi-page) |
| Schemas | Pydantic v2 |

---

## 📁 Key Files

- [`backend/services/llm_service.py`](backend/services/llm_service.py) — Groq API wrapper
- [`backend/services/prompt_service.py`](backend/services/prompt_service.py) — All system prompts
- [`backend/utils/auth.py`](backend/utils/auth.py) — JWT helpers
- [`frontend/utils/api.py`](frontend/utils/api.py) — Frontend API client + shared CSS

---

## 🛡️ Security Notes

- Never commit your `.env` file — it's in `.gitignore`
- Change `SECRET_KEY` to a strong random value in production
- Tighten CORS `allow_origins` in `backend/main.py` for production deployment

---

*Built with ❤️ using FastAPI, Groq, and Streamlit*
