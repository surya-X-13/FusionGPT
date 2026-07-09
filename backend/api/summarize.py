from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.database import get_db
from database import models
from schemas.ai_tools import SummarizeRequest, SummarizeResponse
from services import llm_service, prompt_service
from utils.auth import get_current_user

router = APIRouter(prefix="/summarize", tags=["Summarizer"])

_LENGTH_MAP = {
    "short": "2-3 sentences",
    "medium": "1-2 short paragraphs",
    "long": "a detailed multi-paragraph summary",
}


@router.post("/", response_model=SummarizeResponse)
def summarize(
    request: SummarizeRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Summarize text into short, medium, or long summaries (powered by LangChain + ChatGroq)."""
    target_length = _LENGTH_MAP.get(request.length, "1-2 short paragraphs")
    prompt = prompt_service.summarize_prompt_template()

    try:
        summary, tokens = llm_service.run_chain(
            prompt_template=prompt,
            input_vars={"target_length": target_length, "text": request.text},
            temperature=0.4,
            max_tokens=1024,
        )
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"LLM service error: {str(e)}")

    log = models.UsageLog(
        user_id=current_user.id,
        feature="summarize",
        input_text=request.text[:1000],
        output_text=summary[:2000],
        tokens_used=tokens,
    )
    db.add(log)
    db.commit()

    return SummarizeResponse(summary=summary, tokens_used=tokens)
