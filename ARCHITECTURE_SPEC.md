# Noor System Architecture Specification (EPIC 06)
**Architecture Pattern:** Modular Monolith with Unified Reactive State  
**Frontend:** Next.js (App Router) + TypeScript + Tailwind CSS (PN-18 Tokens)  
**Backend:** FastAPI (Python 3.12) + SQLAlchemy Async + SQLite/PostgreSQL  

---

## 1. High-Level Architecture Diagram

```
+-------------------------------------------------------------+
|                      Noor Web / PWA                         |
|   Next.js 16 (App Router) + React + TypeScript + Tailwind   |
+-------------------------------------------------------------+
        |                                       |
        | (REST JSON API)                       | (Local Storage Cache / Offline Fallback)
        v                                       v
+-------------------------------+       +------------------------------------+
|        FastAPI Monolith       |       | Browser Secure Storage             |
|   /api/v1/identity            |       | - Encrypted Journal Offline Drafts |
|   /api/v1/journal             |       | - Active Consents & Quiet Mode     |
|   /api/v1/companion           |       | - Companion Local Progress Cache   |
|   /api/v1/activities          |       +------------------------------------+
|   /api/v1/community           |
|   /api/v1/memory              |
|   /api/v1/insights            |
|   /api/v1/safety              |
+-------------------------------+
        |
        v
+-------------------------------------------------------------+
|              Authoritative Relational Database              |
|       (SQLAlchemy Async: SQLite [Dev] / PostgreSQL [Prod])   |
|                                                             |
|  - users                 - companion                        |
|  - consent_records       - activity_sessions                |
|  - journal_entries       - community_posts & reactions      |
|  - memory_items          - content_reports                  |
|  - insight_records                                          |
+-------------------------------------------------------------+
```

---

## 2. Service Boundaries & Data Isolation Rules

1. **The Backend is Authoritative:**
   - Permissions, safety evaluations, deterministic progression calculations, and ownership assertions are verified server-side.
2. **Sensitive Data Isolation:**
   - `journal_entries` cannot be queried by community feeds or public APIs.
   - Deleting an entry triggers soft or hard purges of all related derived insights.
3. **Safety Layer Independence:**
   - Safety checks (`/safety/evaluate`) run independently of any generative LLM response to prevent prompt injection bypasses.
4. **Deterministic Insights Engine:**
   - Insights require verifiable evidence summaries from structured session tables before displaying.
