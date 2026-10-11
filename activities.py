from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from typing import List, Dict, Any
from backend.app.core.database import get_db
from backend.app.models.entities import User, ActivitySession, Companion
from backend.app.schemas.schemas import ActivitySessionCreate, ActivitySessionResponse
from backend.app.routers.identity import get_current_user

router = APIRouter(prefix="/activities", tags=["Activities"])

ACTIVITY_CATALOG = [
    {
        "id": "breathing_garden",
        "title": "Breathing Garden",
        "category": "Calm",
        "tagline": "A gentle visual flower rhythm paced by calming breathing cycles.",
        "description": "Follow the natural expansion and contraction of organic petals. No scores, no failures.",
        "default_duration_seconds": 180,
        "is_recreational": True
    },
    {
        "id": "mood_canvas",
        "title": "Mood Canvas",
        "category": "Express",
        "tagline": "Express emotion through fluid color, shape, and brush strokes.",
        "description": "A quiet visual canvas to translate feelings into color without needing words.",
        "default_duration_seconds": 300,
        "is_recreational": True
    },
    {
        "id": "gentle_puzzle",
        "title": "Gentle Puzzle",
        "category": "Distract",
        "tagline": "A soft, low-pressure soothing tile realignment.",
        "description": "Unwind mental tension with tactile patterns. Take all the time you need.",
        "default_duration_seconds": 240,
        "is_recreational": True
    },
    {
        "id": "sort_thoughts",
        "title": "Sort Your Thoughts",
        "category": "Reflect",
        "tagline": "Gently sort concerns into control, influence, and letting go.",
        "description": "Separate what is in your hands from what you can gracefully release.",
        "default_duration_seconds": 360,
        "is_recreational": True
    }
]

@router.get("/catalog")
async def get_catalog():
    return {
        "activities": ACTIVITY_CATALOG,
        "disclaimer": "Activities in Noor are recreational and reflective self-care tools and do not substitute clinical interventions."
    }

@router.post("/sessions", response_model=ActivitySessionResponse, status_code=status.HTTP_201_CREATED)
async def complete_session(
    payload: ActivitySessionCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    session = ActivitySession(
        user_id=current_user.id,
        activity_id=payload.activity_id,
        duration_seconds=payload.duration_seconds,
        completed=payload.completed,
        reflection_note=payload.reflection_note
    )
    db.add(session)

    # Award gentle companion progression for engaging in self-care
    comp_res = await db.execute(select(Companion).where(Companion.user_id == current_user.id))
    companion = comp_res.scalars().first()
    if companion:
        companion.exp += 25
        if companion.exp >= 100:
            companion.level += 1
            companion.exp -= 100

    await db.commit()
    await db.refresh(session)
    return session

@router.get("/sessions", response_model=List[ActivitySessionResponse])
async def list_recent_sessions(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(ActivitySession)
        .where(ActivitySession.user_id == current_user.id)
        .order_by(desc(ActivitySession.created_at))
        .limit(20)
    )
    return result.scalars().all()
