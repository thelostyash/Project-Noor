from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Dict, Any
from backend.app.core.database import get_db
from backend.app.models.entities import User, ConsentRecord, Companion
from backend.app.schemas.schemas import UserCreate, UserResponse, ConsentUpdate, ConsentResponse

router = APIRouter(prefix="/identity", tags=["Identity & Consent"])

# Standard mock current user dependency for local/MVP monolith
async def get_current_user(db: AsyncSession = Depends(get_db)) -> User:
    result = await db.execute(select(User).limit(1))
    user = result.scalars().first()
    if not user:
        user = User(email="seeker@noor.app", nickname="Seeker")
        db.add(user)
        await db.commit()
        await db.refresh(user)

        # Initialize default consents
        default_scopes = [
            ("personalization", False),
            ("ai_analysis", False),
            ("analytics", True),
            ("model_training", False)  # Strictly separated per EPIC 03
        ]
        for scope, granted in default_scopes:
            db.add(ConsentRecord(user_id=user.id, scope=scope, granted=granted))
        
        # Initialize default companion
        companion = Companion(user_id=user.id, name="Noori", companion_type="sprout", trait="gentle")
        db.add(companion)
        await db.commit()
    return user

@router.get("/me", response_model=UserResponse)
async def get_profile(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/consents", response_model=List[ConsentResponse])
async def get_consents(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(ConsentRecord).where(ConsentRecord.user_id == current_user.id))
    return result.scalars().all()

@router.post("/consents", response_model=ConsentResponse)
async def update_consent(
    payload: ConsentUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Rule: model_training consent must never be forced or automatically tied to personalization
    result = await db.execute(
        select(ConsentRecord)
        .where(ConsentRecord.user_id == current_user.id, ConsentRecord.scope == payload.scope)
    )
    consent = result.scalars().first()
    if not consent:
        consent = ConsentRecord(user_id=current_user.id, scope=payload.scope, granted=payload.granted)
        db.add(consent)
    else:
        consent.granted = payload.granted
    
    await db.commit()
    await db.refresh(consent)
    return consent

@router.post("/export-data")
async def export_user_data(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """EPIC 07: Data export workflow - full transparency of user-held records"""
    # Fetch all records
    consents = (await db.execute(select(ConsentRecord).where(ConsentRecord.user_id == current_user.id))).scalars().all()
    companion = (await db.execute(select(Companion).where(Companion.user_id == current_user.id))).scalars().first()
    
    return {
        "user": {
            "id": current_user.id,
            "email": current_user.email,
            "nickname": current_user.nickname,
            "created_at": current_user.created_at.isoformat()
        },
        "consents": [{"scope": c.scope, "granted": c.granted, "updated_at": c.updated_at.isoformat()} for c in consents],
        "companion": {
            "name": companion.name if companion else "Noori",
            "type": companion.companion_type if companion else "sprout",
            "level": companion.level if companion else 1
        }
    }

@router.delete("/delete-account", status_code=status.HTTP_200_OK)
async def delete_account(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """EPIC 07: Complete account deletion - cascades and purges all personal data"""
    await db.delete(current_user)
    await db.commit()
    return {"status": "success", "message": "All user data and derived records have been completely purged."}
