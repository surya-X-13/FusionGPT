from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.database import get_db
from database import models
from schemas.ai_tools import ResumeRequest, ResumeResponse
from services import llm_service, prompt_service
from utils.auth import get_current_user

router = APIRouter(prefix="/resume", tags=["Resume Builder"])


@router.post("/", response_model=ResumeResponse)
def build_resume(
    request: ResumeRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Generate professional resume content including summary and bullet points (powered by LangChain + ChatGroq)."""
    user_content = (
        f"Job Title: {request.job_title}\n"
        f"Years of Experience: {request.years_experience}\n"
        f"Key Skills: {request.key_skills}\n"
    )
    if request.recent_role:
        user_content += f"Most Recent Role: {request.recent_role}\n"
    if request.achievements:
        user_content += f"Key Achievements / Responsibilities: {request.achievements}\n"

    prompt = prompt_service.resume_prompt_template()

    try:
        resume_content, tokens = llm_service.run_chain(
            prompt_template=prompt,
            input_vars={"user_content": user_content},
            temperature=0.5,
            max_tokens=2000,
        )
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"LLM service error: {str(e)}")

    log = models.UsageLog(
        user_id=current_user.id,
        feature="resume",
        input_text=f"{request.job_title} | {request.key_skills}"[:1000],
        output_text=resume_content[:2000],
        tokens_used=tokens,
    )
    db.add(log)
    db.commit()

    return ResumeResponse(resume_content=resume_content, tokens_used=tokens)
