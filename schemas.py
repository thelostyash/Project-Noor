from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
import datetime

# User & Consent
class UserBase(BaseModel):
    email: str
    nickname: str = "Seeker"
    quiet_mode_default: bool = False

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: str
    created_at: datetime.datetime
    model_config = ConfigDict(from_attributes=True)

class ConsentUpdate(BaseModel):
    scope: str = Field(..., description="personalization | ai_analysis | analytics | model_training")
    granted: bool

class ConsentResponse(BaseModel):
    id: str
    scope: str
    granted: bool
    version: str
    updated_at: datetime.datetime
    model_config = ConfigDict(from_attributes=True)

# Journal / My Space
class JournalEntryCreate(BaseModel):
    title: Optional[str] = ""
    content: str
    mood_tag: Optional[str] = None
    analysis_consent: bool = False

class JournalEntryUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    mood_tag: Optional[str] = None
    analysis_consent: Optional[bool] = None

class JournalEntryResponse(BaseModel):
    id: str
    user_id: str
    title: str
    content: str
    mood_tag: Optional[str]
    analysis_consent: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime
    model_config = ConfigDict(from_attributes=True)

class ReflectionRequest(BaseModel):
    entry_id: str
    prompt_intent: Optional[str] = "gentle_summary"

class ReflectionResponse(BaseModel):
    entry_id: str
    reflection_text: str
    grounding_note: str

# Companion
class CompanionUpdate(BaseModel):
    name: Optional[str] = None
    companion_type: Optional[str] = None
    trait: Optional[str] = None
    environment: Optional[str] = None

class CompanionResponse(BaseModel):
    id: str
    user_id: str
    name: str
    companion_type: str
    trait: str
    environment: str
    level: int
    exp: int
    unlocked_items: List[str]
    created_at: datetime.datetime
    updated_at: datetime.datetime
    model_config = ConfigDict(from_attributes=True)

# Activities
class ActivitySessionCreate(BaseModel):
    activity_id: str
    duration_seconds: int = 0
    completed: bool = True
    reflection_note: Optional[str] = None

class ActivitySessionResponse(BaseModel):
    id: str
    user_id: str
    activity_id: str
    duration_seconds: int
    completed: bool
    reflection_note: Optional[str]
    created_at: datetime.datetime
    model_config = ConfigDict(from_attributes=True)

# Community
class CommunityPostCreate(BaseModel):
    content: str = Field(..., max_length=500)
    author_pseudonym: Optional[str] = "Kind Soul"
    is_anonymous: bool = True

class CommunityPostResponse(BaseModel):
    id: str
    author_pseudonym: str
    is_anonymous: bool
    content: str
    reaction_counts: Dict[str, int]
    status: str
    created_at: datetime.datetime
    model_config = ConfigDict(from_attributes=True)

class ReactionCreate(BaseModel):
    reaction_type: str = Field(..., description="heart | hug | strength | calm")

class ReportCreate(BaseModel):
    reason: str = Field(..., max_length=255)

# Memory
class MemoryCreate(BaseModel):
    category: str = Field(..., description="preference | topic | goal")
    content: str
    source: str = "explicit"

class MemoryResponse(BaseModel):
    id: str
    category: str
    content: str
    source: str
    created_at: datetime.datetime
    model_config = ConfigDict(from_attributes=True)

# Insights
class InsightResponse(BaseModel):
    id: str
    title: str
    observation: str
    evidence_summary: str
    category: str
    dismissed: bool
    created_at: datetime.datetime
    model_config = ConfigDict(from_attributes=True)

# Safety / Crisis
class CrisisResource(BaseModel):
    name: str
    contact: str
    description: str
    category: str
    available_hours: str
