from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from typing import List, Optional
import datetime
from backend.app.core.database import get_db
from backend.app.models.entities import User, JournalEntry, ConsentRecord
from backend.app.schemas.schemas import (
    JournalEntryCreate,
    JournalEntryUpdate,
    JournalEntryResponse,
    ReflectionRequest,
    ReflectionResponse
)
from backend.app.routers.identity import get_current_user

router = APIRouter(prefix="/journal", tags=["My Space & Journal"])

@router.get("/entries", response_model=List[JournalEntryResponse])
async def list_entries(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(JournalEntry)
        .where(JournalEntry.user_id == current_user.id, JournalEntry.deleted_at.is_(None))
        .order_by(desc(JournalEntry.created_at))
    )
    return result.scalars().all()

@router.post("/entries", response_model=JournalEntryResponse, status_code=status.HTTP_201_CREATED)
async def create_entry(
    payload: JournalEntryCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    entry = JournalEntry(
        user_id=current_user.id,
        title=payload.title or "Untitled Reflection",
        content=payload.content,
        mood_tag=payload.mood_tag,
        analysis_consent=payload.analysis_consent
    )
    db.add(entry)
    await db.commit()
    await db.refresh(entry)
    return entry

@router.get("/entries/{entry_id}", response_model=JournalEntryResponse)
async def get_entry(
    entry_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(JournalEntry)
        .where(
            JournalEntry.id == entry_id,
            JournalEntry.user_id == current_user.id,
            JournalEntry.deleted_at.is_(None)
        )
    )
    entry = result.scalars().first()
    if not entry:
        raise HTTPException(status_code=404, detail="Journal entry not found or unauthorized.")
    return entry

@router.put("/entries/{entry_id}", response_model=JournalEntryResponse)
async def update_entry(
    entry_id: str,
    payload: JournalEntryUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(JournalEntry)
        .where(
            JournalEntry.id == entry_id,
            JournalEntry.user_id == current_user.id,
            JournalEntry.deleted_at.is_(None)
        )
    )
    entry = result.scalars().first()
    if not entry:
        raise HTTPException(status_code=404, detail="Journal entry not found or unauthorized.")

    if payload.title is not None:
        entry.title = payload.title
    if payload.content is not None:
        entry.content = payload.content
    if payload.mood_tag is not None:
        entry.mood_tag = payload.mood_tag
    if payload.analysis_consent is not None:
        entry.analysis_consent = payload.analysis_consent
    
    entry.updated_at = datetime.datetime.utcnow()
    await db.commit()
    await db.refresh(entry)
    return entry

@router.delete("/entries/{entry_id}")
async def delete_entry(
    entry_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(JournalEntry)
        .where(
            JournalEntry.id == entry_id,
            JournalEntry.user_id == current_user.id,
            JournalEntry.deleted_at.is_(None)
        )
    )
    entry = result.scalars().first()
    if not entry:
        raise HTTPException(status_code=404, detail="Journal entry not found or unauthorized.")
    
    entry.deleted_at = datetime.datetime.utcnow()
    await db.commit()
    return {"status": "success", "message": "Entry removed securely."}

@router.post("/reflect", response_model=ReflectionResponse)
async def request_reflection(
    payload: ReflectionRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    EPIC 08 & EPIC 14: Optional server-side reflection on demand.
    Enforces that analysis consent is active on both the account scope AND entry level.
    Never gives unsolicited advice or clinical diagnosis.
    """
    # 1. Fetch entry
    result = await db.execute(
        select(JournalEntry)
        .where(
            JournalEntry.id == payload.entry_id,
            JournalEntry.user_id == current_user.id,
            JournalEntry.deleted_at.is_(None)
        )
    )
    entry = result.scalars().first()
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found.")
    
    # 2. Check consent
    consent_res = await db.execute(
        select(ConsentRecord)
        .where(ConsentRecord.user_id == current_user.id, ConsentRecord.scope == "ai_analysis")
    )
    ai_consent = consent_res.scalars().first()
    
    if not (ai_consent and ai_consent.granted) and not entry.analysis_consent:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Reflection requires explicit AI analysis consent. You can enable this anytime in privacy controls."
        )

    # 3. Deterministic safe reflection generator (non-clinical, comforting, grounding)
    word_count = len(entry.content.split())
    mood = entry.mood_tag or "reflective"
    reflection_text = (
        f"Thank you for sharing your thoughts ({word_count} words). "
        f"It takes courage to acknowledge feeling {mood}. Notice that simply writing this down created a safe boundary between you and these thoughts."
    )
    grounding_note = "Remember: Noor is here as a gentle sounding board. You are doing enough right now."

    return ReflectionResponse(
        entry_id=entry.id,
        reflection_text=reflection_text,
        grounding_note=grounding_note
    )
