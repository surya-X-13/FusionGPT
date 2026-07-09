from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.database import get_db
from database import models
from schemas.ai_tools import CodeRequest, CodeResponse
from services import llm_service, prompt_service
from utils.auth import get_current_user

router = APIRouter(prefix="/code", tags=["Code Generator"])


@router.post("/", response_model=CodeResponse)
def generate_code(
    request: CodeRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Generate or explain code in any programming language (powered by LangChain + ChatGroq)."""
    # Build user-facing content depending on task type
    if request.task == "explain" and request.code_to_explain:
        user_content = (
            f"Explain this {request.language} code:\n\n"
            f"```{request.language.lower()}\n{request.code_to_explain}\n```"
        )
    else:
        user_content = f"Language: {request.language}\n\nTask: {request.description}"

    prompt = prompt_service.code_prompt_template()

    try:
        result, tokens = llm_service.run_chain(
            prompt_template=prompt,
            input_vars={
                "language": request.language,
                "task_type": request.task,
                "user_content": user_content,
            },
            temperature=0.3,
            max_tokens=3000,
        )
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"LLM service error: {str(e)}")

    log = models.UsageLog(
        user_id=current_user.id,
        feature="code",
        input_text=request.description[:1000] if request.description else user_content[:1000],
        output_text=result[:2000],
        tokens_used=tokens,
    )
    db.add(log)
    db.commit()

    return CodeResponse(result=result, language=request.language, tokens_used=tokens)
