# IdeaJET

> Turn a single-sentence idea into a **Market Brief**, a **1-page PRD**, and a **static Landing Page** — in one run. **Python-only**. **FastAPI + CrewAI**. **Docker-ready.**

---

## What it produces

- **Market Brief (Markdown)**  
  TAM/SAM/SOM (with assumptions), top 5 competitors, source links
- **PRD (Markdown)**  
  Problem, target users, exactly 3 MVP features, user stories, acceptance criteria, risks
- **Landing Page (HTML)**  
  Headline, 3–5 bullets, “Join waitlist” form (server-handled)

---

## How it works (agents)

- **Planner** → scopes steps, assumptions, search queries  
- **Market Analyst** → searches web, skims 2–3 competitor pages, writes the Market Brief  
- **Product Designer** → drafts the 1-page PRD + landing page copy blocks  
- **Page Builder** → renders a clean static HTML page from the copy

```mermaid
flowchart LR
    A[Idea] --> P[Planner]
    P --> M[Market Analyst]
    P --> D[Product Designer]
    D --> B[Page Builder]
    M -->|Brief.md| O1[outputs/]
    D -->|PRD.md| O1
    B -->|landing/index.html| O1
