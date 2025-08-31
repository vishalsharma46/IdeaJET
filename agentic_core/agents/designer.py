# agents/designer.py
from crewai import Agent, Task

def build_agent() -> Agent:
    return Agent(
        role="Product Designer",
        goal=("Write a crisp 1-page PRD: problem, target users, exactly 3 MVP features, "
              "user stories, acceptance criteria, and key risks."),
        backstory=("Zero-fluff UX thinker. Keeps scope tiny, stories testable, "
                   "and acceptance criteria unambiguous."),
        allow_delegation=False,
        verbose=True,
    )

def prd_task(
    idea: str,
    market_brief_md: str = "",
    agent: Agent | None = None
) -> Task:
    agent = agent or build_agent()
    return Task(
        description=(
            f"Draft a 1-page PRD for: `{idea}`.\n"
            "Use any signal from the Market Brief below if provided.\n"
            "=== MARKET BRIEF START ===\n"
            f"{market_brief_md}\n"
            "=== MARKET BRIEF END ===\n\n"
            "PRD sections (Markdown):\n"
            "1) Problem\n"
            "2) Target users\n"
            "3) Exactly 3 MVP features (bullets)\n"
            "4) User stories (Given/When/Then, 4–6 items)\n"
            "5) Acceptance criteria (clear, testable, 6–10 items)\n"
            "6) Risks (3–5 bullets)\n"
            "Keep the total under 600 words."
        ),
        agent=agent,
        expected_output="A single markdown page with the six sections."
    )
