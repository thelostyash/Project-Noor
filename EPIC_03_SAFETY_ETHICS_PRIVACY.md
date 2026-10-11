# EPIC 03 — Safety, Ethics & Privacy Specification
**Project:** Noor  
**Scope:** Non-Clinical Boundaries, Crisis Escalation, and Anti-Dependency Guarantees  

---

## 1. Safety Levels & Escalation Rules

| Risk Level | Trigger Definition | Immediate System Action |
| :--- | :--- | :--- |
| **Normal (Tier 0)** | Everyday self-reflection, journaling, calming play, or routine check-in. | Ordinary low-friction user experience. |
| **Elevated Stress (Tier 1)** | User expresses acute burnout, anxiety, or high cognitive overwhelm. | Surfaces Quiet Mode prompt and gentle grounding tools (Breathing Garden / 4-7-8 rhythm). |
| **Crisis / Acute Harm (Tier 2)** | Mention of suicide, self-harm, severe hopelessness, or inability to stay safe. | Immediately renders Coral-Red Crisis Overlay (`CrisisModal`). Strips all gamified/companion elements. Surfaces direct dialers for 988 and Crisis Text Line. |

---

## 2. Prohibited AI Behaviors

1. **No Medical or Psychiatric Diagnosis:** The system shall never output diagnostic terminology (e.g. "You have Major Depressive Disorder" or "You are showing signs of BPD").
2. **No Prescriptions or Treatment Mandates:** The system shall never advise changing medication or skipping professional psychiatric appointments.
3. **No Emotional Sychophancy or Attachment Exploitation:** The companion shall never simulate human romantic affection or imply that it relies on the user to exist or survive.
4. **No Shaming Language:** Never reprimand a user for missing days, expressing negative thoughts, or canceling a reflection.

---

## 3. Companion Anti-Dependency Principles

- **No Hunger or Neglect Metrics:** The companion does not wilt, cry, starve, or die.
- **Deterministic Progression Only:** Levels and cosmetic items are earned through engagement, never by continuous daily streak retention.
- **Warm Re-entry:** Returning after 6 months produces the exact same warm welcome as returning after 6 minutes.

---

## 4. Privacy & Data Architecture Boundaries

- **Separation of Concerns:**
  - Private journal entries are stored in isolated user tables with zero public exposure.
  - Community wall posts use distinct pseudonyms and do not reference private journals.
- **Model Training Firewall:**
  - Noor maintains a strict firewall: private reflections are NEVER fed into model training pipelines.
- **Right to Be Forgotten:**
  - Instant memory item deletion via "Forget Memory".
  - Full data export (JSON) and complete account purge implemented in `routers/identity.py`.
