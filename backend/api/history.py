from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List

from database.database import get_db
from database import models
from schemas.ai_tools import UsageLogResponse
from utils.auth import get_current_user

router = APIRouter(prefix="/history", tags=["Usage History"])


@router.get("/", response_model=List[UsageLogResponse])
def get_history(
    limit: int = Query(default=50, le=200),
    feature: str = Query(default=None, description="Filter by feature name"),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Retrieve the authenticated user's AI usage history."""
    query = db.query(models.UsageLog).filter(models.UsageLog.user_id == current_user.id)

    if feature:
        query = query.filter(models.UsageLog.feature == feature)

    logs = query.order_by(models.UsageLog.created_at.desc()).limit(limit).all()

    return [
        UsageLogResponse(
            id=log.id,
            feature=log.feature,
            input_text=log.input_text,
            output_text=log.output_text,
            tokens_used=log.tokens_used,
            created_at=log.created_at.isoformat(),
        )
        for log in logs
    ]


@router.get("/stats")
def get_stats(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Return aggregate usage statistics for the current user."""
    logs = db.query(models.UsageLog).filter(models.UsageLog.user_id == current_user.id).all()

    total_requests = len(logs)
    total_tokens = sum(log.tokens_used for log in logs)

    feature_counts: dict = {}
    for log in logs:
        feature_counts[log.feature] = feature_counts.get(log.feature, 0) + 1

    return {
        "total_requests": total_requests,
        "total_tokens_used": total_tokens,
        "feature_breakdown": feature_counts,
        "tier": current_user.tier,
    }
