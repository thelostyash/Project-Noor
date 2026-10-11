import datetime
import uuid
from sqlalchemy import Column, String, Boolean, DateTime, Integer, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from backend.app.core.database import Base

def generate_uuid():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    email = Column(String(255), unique=True, index=True, nullable=False)
    nickname = Column(String(100), default="Seeker")
    quiet_mode_default = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    consents = relationship("ConsentRecord", back_populates="user", cascade="all, delete-orphan")
    journal_entries = relationship("JournalEntry", back_populates="user", cascade="all, delete-orphan")
    companion = relationship("Companion", back_populates="user", uselist=False, cascade="all, delete-orphan")
    activity_sessions = relationship("ActivitySession", back_populates="user", cascade="all, delete-orphan")
    memories = relationship("MemoryItem", back_populates="user", cascade="all, delete-orphan")
    insights = relationship("InsightRecord", back_populates="user", cascade="all, delete-orphan")

class ConsentRecord(Base):
    __tablename__ = "consent_records"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    scope = Column(String(50), nullable=False)  # personalization, ai_analysis, analytics, model_training
    granted = Column(Boolean, default=False, nullable=False)
    version = Column(String(20), default="1.0")
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    user = relationship("User", back_populates="consents")

class JournalEntry(Base):
    __tablename__ = "journal_entries"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), default="")
    content = Column(Text, nullable=False)
    mood_tag = Column(String(50), nullable=True)
    analysis_consent = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="journal_entries")

class Companion(Base):
    __tablename__ = "companions"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    name = Column(String(100), default="Noori")
    companion_type = Column(String(50), default="sprout")  # sprout, ember, pebble, cloud
    trait = Column(String(50), default="gentle")  # gentle, thoughtful, playful
    environment = Column(String(50), default="zen_garden")  # zen_garden, warm_cafe, cozy_attic
    level = Column(Integer, default=1)
    exp = Column(Integer, default=0)
    unlocked_items = Column(JSON, default=list)  # list of cosmetic item IDs
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    user = relationship("User", back_populates="companion")

class ActivitySession(Base):
    __tablename__ = "activity_sessions"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    activity_id = Column(String(100), nullable=False)  # breathing_garden, mood_canvas, gentle_puzzle, sort_thoughts
    duration_seconds = Column(Integer, default=0)
    completed = Column(Boolean, default=True)
    reflection_note = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="activity_sessions")

class CommunityPost(Base):
    __tablename__ = "community_posts"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    author_pseudonym = Column(String(100), default="Kind Heart")
    is_anonymous = Column(Boolean, default=True)
    content = Column(Text, nullable=False)
    reaction_counts = Column(JSON, default=lambda: {"heart": 0, "hug": 0, "strength": 0, "calm": 0})
    status = Column(String(30), default="published")  # published, under_review, removed
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    reactions = relationship("PostReaction", back_populates="post", cascade="all, delete-orphan")
    reports = relationship("ContentReport", back_populates="post", cascade="all, delete-orphan")

class PostReaction(Base):
    __tablename__ = "post_reactions"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    post_id = Column(String(36), ForeignKey("community_posts.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    reaction_type = Column(String(30), nullable=False)  # heart, hug, strength, calm
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    post = relationship("CommunityPost", back_populates="reactions")

class ContentReport(Base):
    __tablename__ = "content_reports"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    post_id = Column(String(36), ForeignKey("community_posts.id", ondelete="CASCADE"), nullable=False, index=True)
    reporter_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    reason = Column(String(255), nullable=False)
    status = Column(String(30), default="open")  # open, actioned, dismissed
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    post = relationship("CommunityPost", back_populates="reports")

class MemoryItem(Base):
    __tablename__ = "memory_items"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    category = Column(String(50), nullable=False)  # preference, topic, goal
    content = Column(Text, nullable=False)
    source = Column(String(50), default="explicit")  # explicit, checkin, reflection
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="memories")

class InsightRecord(Base):
    __tablename__ = "insight_records"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    observation = Column(Text, nullable=False)
    evidence_summary = Column(Text, nullable=False)
    category = Column(String(50), default="routine")  # routine, mood_trend, activity_impact
    dismissed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="insights")
