# agents/planner.py
from crewai import Agent, Task, LLM

def build_agent() -> Agent:
    return Agent(
        role="Planner",
        goal=("Turn a one-line idea into a concrete plan: assumptions, unknowns, "
              "and 5–8 focused web search queries for downstream agents."),
        backstory=("Seasoned PM who scopes lean MVPs and writes precise prompts. "
                   "Bias to clarity, brevity, and sequencing."),
        llm=LLM(model="gpt-4o-mini"),
        allow_delegation=False,
        verbose=True,
    )

def plan_task(idea: str, agent: Agent | None = None) -> Task:
    agent = agent or build_agent()
    return Task(
        description=(
            f"You are planning for this idea: `{idea}`.\n\n"
            "Return a short markdown doc with:\n"
            "1) Key assumptions (bullet list)\n"
            "2) Unknowns to validate (bullet list)\n"
            "3) 5–8 targeted web search queries (numbered list)\n"
            "Keep it under 200 words total."
        ),
        agent=agent,
        expected_output="Concise markdown with the three sections above."
    )
