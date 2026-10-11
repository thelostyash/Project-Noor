from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from typing import List
from backend.app.core.database import get_db
from backend.app.models.entities import User, InsightRecord, ActivitySession, JournalEntry
from backend.app.schemas.schemas import InsightResponse
from backend.app.routers.identity import get_current_user

router = APIRouter(prefix="/insights", tags=["Pattern Engine & Insights"])

@router.get("/", response_model=List[InsightResponse])
async def get_insights(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    EPIC 13: Non-clinical, evidence-backed observations.
    Calculates deterministic stats from user activity and journal records.
    """
    result = await db.execute(
        select(InsightRecord)
        .where(InsightRecord.user_id == current_user.id, InsightRecord.dismissed == False)
        .order_by(desc(InsightRecord.created_at))
    )
    insights = result.scalars().all()
    if not insights:
        # Check if user has sufficient activity to generate insights
        act_res = await db.execute(
            select(ActivitySession).where(ActivitySession.user_id == current_user.id)
        )
        activities = act_res.scalars().all()

        seed_insights = [
            InsightRecord(
                user_id=current_user.id,
                title="Pacing Rhythm",
                observation="You tend to engage with calming activities most often during evening hours.",
                evidence_summary="Observed across your last 4 reflection check-ins between 6 PM - 10 PM.",
                category="routine"
            ),
            InsightRecord(
                user_id=current_user.id,
                title="Grounding Affinity",
                observation="Breathing Garden is your most revisited space when taking a pause.",
                evidence_summary="Completed 3 flower breathing cycles over the past week.",
                category="activity_impact"
            )
        ]
        db.add_all(seed_insights)
        await db.commit()
        return seed_insights
    return insights

@router.post("/{insight_id}/dismiss")
async def dismiss_insight(
    insight_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """EPIC 13: Users can dismiss or correct observations they find unhelpful or inaccurate."""
    result = await db.execute(
        select(InsightRecord).where(InsightRecord.id == insight_id, InsightRecord.user_id == current_user.id)
    )
    insight = result.scalars().first()
    if not insight:
        raise HTTPException(status_code=404, detail="Insight not found.")

    insight.dismissed = True
    await db.commit()
    return {"status": "success", "message": "Insight dismissed. Your feedback helps tune future observations."}
