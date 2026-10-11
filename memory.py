from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from typing import List
from backend.app.core.database import get_db
from backend.app.models.entities import User, MemoryItem, ConsentRecord
from backend.app.schemas.schemas import MemoryCreate, MemoryResponse
from backend.app.routers.identity import get_current_user

router = APIRouter(prefix="/memory", tags=["Memory & Personalization Context"])

@router.get("/", response_model=List[MemoryResponse])
async def get_memories(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """EPIC 12: What Noor remembers - explicit view of all stored memory facts"""
    result = await db.execute(
        select(MemoryItem)
        .where(MemoryItem.user_id == current_user.id)
        .order_by(desc(MemoryItem.created_at))
    )
    items = result.scalars().all()
    if not items:
        # Seed initial transparent default memory items
        seed_items = [
            MemoryItem(
                user_id=current_user.id,
                category="preference",
                content="Prefers quiet evening reflections and gentle pacing.",
                source="explicit"
            ),
            MemoryItem(
                user_id=current_user.id,
                category="goal",
                content="Building a balanced daily breathing routine.",
                source="explicit"
            )
        ]
        db.add_all(seed_items)
        await db.commit()
        return seed_items
    return items

@router.post("/", response_model=MemoryResponse, status_code=status.HTTP_201_CREATED)
async def add_memory(
    payload: MemoryCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Verify personalization consent
    consent_res = await db.execute(
        select(ConsentRecord)
        .where(ConsentRecord.user_id == current_user.id, ConsentRecord.scope == "personalization")
    )
    consent = consent_res.scalars().first()
    if consent and not consent.granted and payload.source != "explicit":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Personalization consent is turned off. Derived memories cannot be stored."
        )

    memory = MemoryItem(
        user_id=current_user.id,
        category=payload.category,
        content=payload.content,
        source=payload.source
    )
    db.add(memory)
    await db.commit()
    await db.refresh(memory)
    return memory

@router.delete("/{memory_id}")
async def forget_memory(
    memory_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """EPIC 12: Forget memory - user right to inspect and purge any memory item"""
    result = await db.execute(
        select(MemoryItem).where(MemoryItem.id == memory_id, MemoryItem.user_id == current_user.id)
    )
    memory = result.scalars().first()
    if not memory:
        raise HTTPException(status_code=404, detail="Memory item not found.")

    await db.delete(memory)
    await db.commit()
    return {"status": "success", "message": "Memory forgotten and removed permanently."}
