from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.database import get_db
from database import models
from schemas.ai_tools import EmailRequest, EmailResponse
from services import llm_service, prompt_service
from utils.auth import get_current_user

router = APIRouter(prefix="/email", tags=["Email Writer"])

_TONE_MAP = {
    "professional": "formal and professional",
    "casual": "friendly and conversational",
    "apologetic": "sincere, empathetic, and apologetic",
    "persuasive": "confident and persuasive",
    "follow_up": "polite and concise",
}


@router.post("/", response_model=EmailResponse)
def write_email(
    request: EmailRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Draft a professional email based on context and tone (powered by LangChain + ChatGroq)."""
    tone_description = _TONE_MAP.get(request.tone, "formal and professional")

    user_content_parts = [f"Email purpose/context: {request.context}"]
    if request.recipient:
        user_content_parts.append(f"Recipient: {request.recipient}")
    if request.additional_info:
        user_content_parts.append(f"Additional details: {request.additional_info}")
    user_content = "\n".join(user_content_parts)

    prompt = prompt_service.email_prompt_template()

    try:
        email_content, tokens = llm_service.run_chain(
            prompt_template=prompt,
            input_vars={"tone_description": tone_description, "user_content": user_content},
            temperature=0.6,
            max_tokens=1500,
        )
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"LLM service error: {str(e)}")

    log = models.UsageLog(
        user_id=current_user.id,
        feature="email",
        input_text=request.context[:1000],
        output_text=email_content[:2000],
        tokens_used=tokens,
    )
    db.add(log)
    db.commit()

    return EmailResponse(email_content=email_content, tokens_used=tokens)
