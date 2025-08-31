# agents/market_analyst.py
from crewai import Agent, Task
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type

# --- Serper wrapper to normalize args ---
# It accepts q="..." and calls Serper with the required search_query="..."
class _SearchArgs(BaseModel):
    q: str = Field(..., description="Web search query")

class WebSearch(BaseTool):
    name: str = "web_search"
    description: str = "Search the web via serper.dev; returns brief titles and URLs."
    args_schema: Type[_SearchArgs] = _SearchArgs

    # Option 1: call crewai_tools (if installed)
    def _run(self, q: str) -> str:
        try:
            from crewai_tools import SerperDevTool
            # SerperDevTool expects: search_query="..."
            return SerperDevTool()._run(search_query=q)
        except Exception:
            # Option 2: fallback to raw HTTP if crewai_tools missing/bugs out
            import os, requests, json
            api_key = os.getenv("SERPER_API_KEY")
            if not api_key:
                return "SERPER_API_KEY not set; cannot search."
            r = requests.post(
                "https://google.serper.dev/search",
                headers={"X-API-KEY": api_key, "Content-Type": "application/json"},
                json={"q": q, "num": 5},
                timeout=20,
            )
            r.raise_for_status()
            data = r.json()
            org = (data.get("organic") or [])[:5]
            lines = [f"{it.get('title','')} - {it.get('link','')}" for it in org]
            return "\n".join(lines) or "No results."

def build_agent() -> Agent:
    return Agent(
        role="Market Analyst",
        goal=("Research the space and produce a tight Market Brief with "
              "TAM/SAM/SOM (state assumptions), top 5 competitors, and source links."),
        backstory=("Analyst who skims fast, cites sources, and triangulates estimates. "
                   "Prefers conservative numbers and clear caveats."),
        tools=[WebSearch()],       # ← use our wrapper tool
        allow_delegation=False,
        verbose=True,
    )

def market_brief_task(
    idea: str,
    planner_notes: str = "",
    agent: Agent | None = None
) -> Task:
    agent = agent or build_agent()
    return Task(
        description=(
            f"Create a Market Brief for idea: `{idea}`.\n"
            f"Planner notes (may be empty):\n{planner_notes}\n\n"
            "Instructions:\n"
            "- Use the web_search tool when you need web data. Call it like: web_search(q=\"your query\").\n"
            "- Do quick research (2–3 competitor pages + market stats).\n"
            "- Estimate TAM/SAM/SOM with explicit assumptions (bullets). Be conservative.\n"
            "- List top 5 competitors with a 1–line positioning.\n"
            "- Provide 5–8 source links at the end.\n"
            "Format: **Markdown**, < 500 words."
        ),
        agent=agent,
        expected_output="Markdown Market Brief with: Overview, TAM/SAM/SOM, Competitors, Sources."
    )
