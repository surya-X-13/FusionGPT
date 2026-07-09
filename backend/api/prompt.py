from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.database import get_db
from database import models
from schemas.ai_tools import PromptRequest, PromptResponse
from services import llm_service, prompt_service
from utils.auth import get_current_user

router = APIRouter(prefix="/prompt", tags=["Prompt Generator"])


@router.post("/", response_model=PromptResponse)
def generate_prompt(
    request: PromptRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Generate an optimized AI prompt for any task or goal (powered by LangChain + ChatGroq)."""
    user_content = f"Goal: {request.goal}"
    if request.context:
        user_content += f"\nContext: {request.context}"
    if request.output_format:
        user_content += f"\nDesired output format: {request.output_format}"

    prompt = prompt_service.prompt_generator_prompt_template()

    try:
        generated, tokens = llm_service.run_chain(
            prompt_template=prompt,
            input_vars={"user_content": user_content},
            temperature=0.7,
            max_tokens=1500,
        )
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"LLM service error: {str(e)}")

    log = models.UsageLog(
        user_id=current_user.id,
        feature="prompt",
        input_text=request.goal[:1000],
        output_text=generated[:2000],
        tokens_used=tokens,
    )
    db.add(log)
    db.commit()

    return PromptResponse(generated_prompt=generated, tokens_used=tokens)
