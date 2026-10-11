from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from backend.app.core.database import get_db
from backend.app.models.entities import User, Companion
from backend.app.schemas.schemas import CompanionUpdate, CompanionResponse
from backend.app.routers.identity import get_current_user

router = APIRouter(prefix="/companion", tags=["Companion"])

@router.get("/", response_model=CompanionResponse)
async def get_companion(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Companion).where(Companion.user_id == current_user.id))
    companion = result.scalars().first()
    if not companion:
        companion = Companion(
            user_id=current_user.id,
            name="Noori",
            companion_type="sprout",
            trait="gentle",
            environment="zen_garden",
            level=1,
            exp=0,
            unlocked_items=["default_glow", "stone_bench"]
        )
        db.add(companion)
        await db.commit()
        await db.refresh(companion)
    return companion

@router.patch("/", response_model=CompanionResponse)
async def update_companion(
    payload: CompanionUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Companion).where(Companion.user_id == current_user.id))
    companion = result.scalars().first()
    if not companion:
        raise HTTPException(status_code=404, detail="Companion not found.")
    
    if payload.name is not None:
        companion.name = payload.name.strip()[:50]
    if payload.companion_type is not None:
        if payload.companion_type in ["sprout", "ember", "pebble", "cloud"]:
            companion.companion_type = payload.companion_type
    if payload.trait is not None:
        if payload.trait in ["gentle", "thoughtful", "playful"]:
            companion.trait = payload.trait
    if payload.environment is not None:
        if payload.environment in ["zen_garden", "warm_cafe", "cozy_attic"]:
            companion.environment = payload.environment

    await db.commit()
    await db.refresh(companion)
    return companion

@router.post("/interact", response_model=CompanionResponse)
async def interact_with_companion(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    EPIC 09: Gentle interaction that rewards gentle reflection.
    Progression is deterministic and never punishes time away.
    """
    result = await db.execute(select(Companion).where(Companion.user_id == current_user.id))
    companion = result.scalars().first()
    if not companion:
        raise HTTPException(status_code=404, detail="Companion not found.")
    
    # Deterministic progression
    companion.exp += 15
    if companion.exp >= 100:
        companion.level += 1
        companion.exp = companion.exp - 100
        # Unlock cosmetic reward
        new_item = f"cosmetic_tier_{companion.level}"
        items = list(companion.unlocked_items or [])
        if new_item not in items:
            items.append(new_item)
            companion.unlocked_items = items
            
    await db.commit()
    await db.refresh(companion)
    return companion
