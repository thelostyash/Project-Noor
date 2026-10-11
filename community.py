from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from typing import List
from backend.app.core.database import get_db
from backend.app.models.entities import User, CommunityPost, PostReaction, ContentReport
from backend.app.schemas.schemas import (
    CommunityPostCreate,
    CommunityPostResponse,
    ReactionCreate,
    ReportCreate
)
from backend.app.routers.identity import get_current_user

router = APIRouter(prefix="/community", tags=["Community Wall & Moderation"])

BANNED_OR_CRISIS_KEYWORDS = [
    "suicide", "kill myself", "end it all", "self harm", "hate you", "die"
]

@router.get("/posts", response_model=List[CommunityPostResponse])
async def get_feed(
    db: AsyncSession = Depends(get_db)
):
    """
    Chronological human feed of published posts.
    No popularity sorting or engagement streaks.
    """
    result = await db.execute(
        select(CommunityPost)
        .where(CommunityPost.status == "published")
        .order_by(desc(CommunityPost.created_at))
        .limit(50)
    )
    posts = result.scalars().all()
    if not posts:
        # Seed initial warm, supportive community posts
        seed_posts = [
            CommunityPost(
                user_id="system-user",
                author_pseudonym="Gentle Breeze",
                is_anonymous=True,
                content="Taking a 5-minute break today felt like catching my breath for the first time all week. Be gentle with yourselves.",
                reaction_counts={"heart": 12, "hug": 8, "strength": 5, "calm": 15},
                status="published"
            ),
            CommunityPost(
                user_id="system-user",
                author_pseudonym="Morning Tea",
                is_anonymous=True,
                content="Reminding anyone who needs to hear it: you don't have to figure everything out today.",
                reaction_counts={"heart": 24, "hug": 19, "strength": 14, "calm": 18},
                status="published"
            )
        ]
        db.add_all(seed_posts)
        await db.commit()
        return seed_posts
    return posts

@router.post("/posts", response_model=CommunityPostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(
    payload: CommunityPostCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Basic server-side pre-moderation scan
    lowered = payload.content.lower()
    post_status = "published"
    for word in BANNED_OR_CRISIS_KEYWORDS:
        if word in lowered:
            post_status = "under_review"
            break

    post = CommunityPost(
        user_id=current_user.id,
        author_pseudonym=payload.author_pseudonym if not payload.is_anonymous else "Kind Traveler",
        is_anonymous=payload.is_anonymous,
        content=payload.content,
        reaction_counts={"heart": 0, "hug": 0, "strength": 0, "calm": 0},
        status=post_status
    )
    db.add(post)
    await db.commit()
    await db.refresh(post)
    return post

@router.post("/posts/{post_id}/react")
async def react_to_post(
    post_id: str,
    payload: ReactionCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    valid_reactions = ["heart", "hug", "strength", "calm"]
    if payload.reaction_type not in valid_reactions:
        raise HTTPException(status_code=400, detail="Invalid reaction type.")

    result = await db.execute(select(CommunityPost).where(CommunityPost.id == post_id))
    post = result.scalars().first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found.")

    counts = dict(post.reaction_counts or {"heart": 0, "hug": 0, "strength": 0, "calm": 0})
    counts[payload.reaction_type] = counts.get(payload.reaction_type, 0) + 1
    post.reaction_counts = counts

    # Record reaction log
    reaction = PostReaction(
        post_id=post_id,
        user_id=current_user.id,
        reaction_type=payload.reaction_type
    )
    db.add(reaction)
    await db.commit()
    return {"status": "success", "reaction_counts": post.reaction_counts}

@router.post("/posts/{post_id}/report", status_code=status.HTTP_201_CREATED)
async def report_post(
    post_id: str,
    payload: ReportCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(CommunityPost).where(CommunityPost.id == post_id))
    post = result.scalars().first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found.")

    report = ContentReport(
        post_id=post_id,
        reporter_id=current_user.id,
        reason=payload.reason
    )
    db.add(report)

    # Automatically set post to under review if reported
    post.status = "under_review"
    await db.commit()

    return {"status": "success", "message": "Thank you for looking out for the community. The post has been flagged for review."}
