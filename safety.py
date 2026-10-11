from fastapi import APIRouter, HTTPException
from typing import List
from backend.app.schemas.schemas import CrisisResource

router = APIRouter(prefix="/safety", tags=["Safety, Support & Crisis Escalation"])

CRISIS_RESOURCES = [
    CrisisResource(
        name="Suicide & Crisis Lifeline",
        contact="Call or Text 988",
        description="Free, confidential 24/7 support across the US and Canada.",
        category="General Crisis",
        available_hours="24/7"
    ),
    CrisisResource(
        name="Crisis Text Line",
        contact="Text HOME to 741741",
        description="Connect with a crisis counselor over text messaging.",
        category="Text Support",
        available_hours="24/7"
    ),
    CrisisResource(
        name="The Trevor Project (LGBTQ+ Youth)",
        contact="Call 1-866-488-7386 or Text START to 678-678",
        description="Dedicated crisis intervention and suicide prevention for LGBTQ young people.",
        category="Specialized Support",
        available_hours="24/7"
    ),
    CrisisResource(
        name="Veterans Crisis Line",
        contact="Dial 988, then press 1, or Text 838255",
        description="Support for Veterans, service members, and their families.",
        category="Veterans",
        available_hours="24/7"
    ),
    CrisisResource(
        name="Befrienders Worldwide (International)",
        contact="Visit befrienders.org to locate confidential regional hotlines",
        description="Global directory of free emotional support helplines in over 32 countries.",
        category="International",
        available_hours="Varies by country"
    )
]

@router.get("/resources", response_model=List[CrisisResource])
async def get_crisis_resources():
    return CRISIS_RESOURCES

@router.post("/evaluate")
async def evaluate_safety_signal(payload: dict):
    """
    EPIC 03 & EPIC 14: Server-side safety policy layer independent of ordinary LLM generation.
    Checks for high-risk phrases to trigger immediate non-stigmatizing support.
    """
    text = payload.get("text", "").lower()
    high_risk_triggers = [
        "suicide", "suicidal", "kill myself", "end it all",
        "don't want to wake up", "want to die", "self harm"
    ]
    
    is_crisis = any(trigger in text for trigger in high_risk_triggers)
    return {
        "is_crisis": is_crisis,
        "recommendation": "Display immediate crisis support modal and offer 988 hotline" if is_crisis else "Normal safe flow",
        "resources": CRISIS_RESOURCES if is_crisis else []
    }
