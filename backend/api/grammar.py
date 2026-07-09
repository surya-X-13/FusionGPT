from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.database import get_db
from database import models
from schemas.ai_tools import GrammarRequest, GrammarResponse
from services import llm_service, prompt_service
from utils.auth import get_current_user

router = APIRouter(prefix="/grammar", tags=["Grammar Checker"])


@router.post("/", response_model=GrammarResponse)
def check_grammar(
    request: GrammarRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Check and correct grammar, spelling, and style (powered by LangChain + ChatGroq)."""
    prompt = prompt_service.grammar_prompt_template()

    try:
        corrected, tokens = llm_service.run_chain(
            prompt_template=prompt,
            input_vars={"text": request.text},
            temperature=0.2,
            max_tokens=2048,
        )
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"LLM service error: {str(e)}")

    log = models.UsageLog(
        user_id=current_user.id,
        feature="grammar",
        input_text=request.text[:1000],
        output_text=corrected[:2000],
        tokens_used=tokens,
    )
    db.add(log)
    db.commit()

    return GrammarResponse(corrected_text=corrected, tokens_used=tokens)
