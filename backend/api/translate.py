from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.database import get_db
from database import models
from schemas.ai_tools import TranslateRequest, TranslateResponse
from services import llm_service, prompt_service
from utils.auth import get_current_user

router = APIRouter(prefix="/translate", tags=["Translator"])


@router.post("/", response_model=TranslateResponse)
def translate(
    request: TranslateRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Translate text to the specified target language (powered by LangChain + ChatGroq)."""
    # Prepend source-language hint when explicitly provided
    text_content = request.text
    if request.source_language and request.source_language.lower() != "auto":
        text_content = f"[Source language: {request.source_language}]\n\n{request.text}"

    prompt = prompt_service.translate_prompt_template()

    try:
        translated, tokens = llm_service.run_chain(
            prompt_template=prompt,
            input_vars={"target_language": request.target_language, "text": text_content},
            temperature=0.3,
            max_tokens=2048,
        )
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"LLM service error: {str(e)}")

    log = models.UsageLog(
        user_id=current_user.id,
        feature="translate",
        input_text=request.text[:1000],
        output_text=translated[:2000],
        tokens_used=tokens,
    )
    db.add(log)
    db.commit()

    return TranslateResponse(
        translated_text=translated,
        target_language=request.target_language,
        tokens_used=tokens,
    )
