from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.database import get_db
from database import models
from schemas.ai_tools import ChatRequest, ChatResponse
from services import llm_service, prompt_service
from utils.auth import get_current_user

router = APIRouter(prefix="/chat", tags=["Chat"])


def _log_usage(db: Session, user_id: int, feature: str, input_text: str, output_text: str, tokens: int):
    log = models.UsageLog(
        user_id=user_id,
        feature=feature,
        input_text=input_text[:1000] if input_text else None,
        output_text=output_text[:2000] if output_text else None,
        tokens_used=tokens,
    )
    db.add(log)
    db.commit()


@router.post("/", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Conversational AI chat with history support (powered by LangChain + ChatGroq)."""
    # Build full message list (system + history + latest user message) and
    # pass through the legacy-compatible generate_text path so that conversation
    # history is preserved exactly as the frontend sends it.
    system_prompt = prompt_service.chat_system_prompt()
    history = [{"role": msg.role, "content": msg.content} for msg in request.history]
    messages = llm_service.build_messages(system_prompt, request.message, history)

    try:
        reply, tokens = llm_service.generate_text(messages, temperature=0.8)
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"LLM service error: {str(e)}")

    _log_usage(db, current_user.id, "chat", request.message, reply, tokens)
    return ChatResponse(reply=reply, tokens_used=tokens)
