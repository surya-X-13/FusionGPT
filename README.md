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


Web App URL = "https://fusiongpt-crqy6upephnwtxd2mappc7i.streamlit.app"
