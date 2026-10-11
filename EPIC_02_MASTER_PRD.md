# EPIC 02 — Master Product Requirements Document (PRD) (Sprint S1)
**Project:** Noor  
**Scope:** MVP Functional & Non-Functional Specifications  
**Author:** Product & Engineering Pair  

---

## 1. System Feature Specifications

### 1.1 Home & Need-State Navigation
- **Intent:** Answer *"What do I need right now?"* upon opening the app.
- **Entry Points:**
  - *I want to write* -> Routes directly to My Space.
  - *I want to relax* -> Routes to Activities framework.
  - *I want to connect* -> Routes to Community Wall.
  - *Spend time with companion* -> Routes to Companion sanctuary.
- **Header:** Houses persistent, distinct coral-red `#C85A52` "Get Help Now" button, Quiet Mode toggle, and theme switch.

### 1.2 My Space: Private Notebook (EPIC 08)
- **Features:** Distraction-free text editor, automatic debounced autosave, title, mood tagging, and list view with search.
- **AI Reflection Boundary:** On-demand only via explicit "Reflect on this" button. Requires both account-level AI consent and per-entry consent. Produces non-clinical summaries with grounding perspective.

### 1.3 Companion: Creation & Deterministic Progression (EPIC 09)
- **Forms:** Sprout (🌱), Ember (🔥), Pebble (🪨), Cloud (☁️).
- **Environments:** Zen Garden, Warm Café, Cozy Attic.
- **Progression:** Rewards reflections and calm activities with XP. Unlocks cosmetic items. No punishment for absence.

### 1.4 Activities & Play Framework (EPIC 10)
- **1. Breathing Garden:** Organic petal bloom synchronized with 4-4-4 and 4-7-8 breathing cues.
- **2. Mood Canvas:** Fluid freeform canvas with warm color palette.
- **3. Gentle Puzzle:** Low-pressure 3x3 pattern alignment with undo and no time limit.
- **4. Sort Your Thoughts:** Cognitive reframing into Control, Influence, and Letting Go.

### 1.5 Community Wall & Moderation (EPIC 11)
- **Format:** Chronological text-only posts with anonymous or nickname attribution.
- **Reactions:** Empathetic supportive reactions (Heart, Hug, Strength, Calm).
- **Safety:** Content pre-moderation scan and user reporting workflow.

### 1.6 Memory & Consent Dashboard (EPIC 12)
- **Transparency:** Direct list of "What Noor Remembers".
- **User Agency:** Instant "Forget Memory" button per item.
- **Scopes:** Granular toggles for Personalization, AI Reflection, Analytics, and Model Training (locked off).

---

## 2. Requirements Traceability Matrix

| Requirement ID | Epic / Pillar | User Story | Backend Implementation | Frontend Implementation | Acceptance Test |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **REQ-ID-01** | Identity & Consent | As a user, I can control how my data is used. | `routers/identity.py` (`/consents`) | `PrivacyModal.tsx` | `test_identity_and_consent_flow` |
| **REQ-JRN-01** | My Space | As a user, I can write privately without unsolicited feedback. | `routers/journal.py` (`/entries`) | `JournalView.tsx` | `test_journal_crud_and_consent_reflection` |
| **REQ-JRN-02** | My Space | As a user, I can request on-demand reflection only when consented. | `routers/journal.py` (`/reflect`) | `JournalView.tsx` | `test_journal_crud_and_consent_reflection` |
| **REQ-CMP-01** | Companion | As a user, I can customize and interact with my companion without guilt. | `routers/companion.py` | `CompanionView.tsx` | `test_companion_progression` |
| **REQ-ACT-01** | Activities | As a user, I can engage in calming activities without score pressure. | `routers/activities.py` | `ActivitiesView.tsx` | `test_activities_and_sessions` |
| **REQ-COM-01** | Community | As a user, I can post anonymously and react supportively. | `routers/community.py` | `CommunityView.tsx` | `test_community_and_moderation` |
| **REQ-SFT-01** | Safety & Support | As a user, I can access crisis hotlines immediately from anywhere. | `routers/safety.py` | `CrisisModal.tsx` | `test_safety_and_crisis_resources` |
