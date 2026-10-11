# Noor — Reflective Wellness App 🌿

Noor is an open, non-clinical digital sanctuary designed for self-expression, gentle play, companion progression, and authentic human connection without algorithmic pressure or clinical pathologizing.

Built according to the **16-Sprint / 20-Epic Noor Roadmap** and the **PN-18 Visual Identity Specification**.

---

## 🎨 Visual Identity & Design Tokens (PN-18)
- **Primary (Terracotta / Sunset Orange):** `#D97757` (hover: `#C46545`)
- **Secondary (Peach / Soft Amber):** `#F4A261`
- **Accent (Muted Clay):** `#E76F51`
- **Light Surface (Warm Cream / Sand):** `#FDFBF7`
- **Dark Surface (Deep Espresso / Charcoal):** `#1A1716`
- **Text (Deep Charcoal / Soft Warm White):** `#2C2523` / `#F4F1EA`
- **Semantic (Gentle Sage):** `#768A74`
- **Safety / Crisis (Coral-Red):** `#C85A52`
- **Typography:** Fraunces (Headings) + Plus Jakarta Sans (Body & UI)
- **Accessibility:** WCAG 2.2 AA compliant contrast, Quiet Mode toggle, Reduced Motion support.

---

## 🏛️ Architecture: Modular Monolith
- **Frontend:** Next.js 16 (App Router) + React 19 + TypeScript + Tailwind CSS v4
- **Backend:** FastAPI (Python 3.12) + SQLAlchemy Async + aiosqlite / PostgreSQL
- **Data Isolation:** Private journal notes, public community feed, and derived memory are logically quarantined.
- **Strict Ethics:** No model training on private notes, zero guilt streaks, and non-clinical crisis escalation hotlines (988).

---

## 🚀 Getting Started

### 1. Run the Python Backend
```powershell
# From the project root
cd "d:\Project Noor"
python -m uvicorn backend.app.main:app --reload --port 8000
```
- API Base: `http://localhost:8000/api/v1`
- Interactive OpenAPI Docs: `http://localhost:8000/docs`
- Run Backend Tests:
  ```powershell
  python -m pytest backend/tests/test_api.py -v
  ```

### 2. Run the Next.js Frontend
```powershell
cd "d:\Project Noor\frontend"
npm run dev
```
- Open in browser: `http://localhost:3000`

---

## 📂 Core Pillars & Implemented Epics
1. **Home (`HomeView.tsx`):** "What do I need right now?" entry points, gentle daily check-in, companion widget.
2. **My Space (`JournalView.tsx`):** Distraction-free notebook, autosave, reflection on demand, zero unsolicited advice.
3. **Activities & Play (`ActivitiesView.tsx`):**
   - *Breathing Garden:* Visual flower bloom pacing 4-4-4 and 4-7-8 breathing cycles.
   - *Mood Canvas:* Fluid color painting canvas with palette controls.
   - *Gentle Puzzle:* Low-pressure 3x3 sliding tile realignment with undo.
   - *Sort Your Thoughts:* Cognitive reframing into Control, Influence, and Letting Go.
4. **Community Wall (`CommunityView.tsx`):** Chronological feed, anonymous posting, supportive reactions (Heart, Hug, Strength, Calm), and safety moderation.
5. **Companion (`CompanionView.tsx`):** 2D customizable avatar (Sprout, Ember, Pebble, Cloud) with deterministic leveling and anti-dependency guarantee.
6. **Privacy & What Noor Remembers (`PrivacyModal.tsx`):** Inspect memories, "Forget Memory", consent toggles, and data export/purge.
7. **Personal Insights (`InsightsModal.tsx`):** Evidence-backed habit observations with "Why am I seeing this?" transparency.
8. **Crisis Safety (`CrisisModal.tsx`):** Global persistent coral-red "Get Help Now" button with 988 hotlines and 4-7-8 grounding.
