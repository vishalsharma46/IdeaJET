# scripts/preview_outputs.py
from pathlib import Path
import sys

from dotenv import load_dotenv
from crewai import Crew, Process

# 1) env + dirs
load_dotenv()
Path("outputs/landing").mkdir(parents=True, exist_ok=True)

# 2) import your agents + task factories
from agentic_core.agents.planner import build_agent as build_planner, plan_task
from agentic_core.agents.market_analyst import build_agent as build_analyst, market_brief_task
from agentic_core.agents.designer import build_agent as build_designer, prd_task
from agentic_core.agents.page_builder import build_agent as build_page_builder, landing_page_task

def to_text(x) -> str:
    # CrewAI may return objects; make sure we always have a string
    return x if isinstance(x, str) else str(x)

def main():
    idea = " ".join(sys.argv[1:]) or "AI-powered resume tailor"

    # ---- Planner ----
    planner = build_planner()
    t_plan = plan_task(idea, agent=planner)
    res_plan = to_text(Crew(agents=[planner], tasks=[t_plan],
                            process=Process.sequential, verbose=True).kickoff())
    print("\n" + "="*18 + " PLANNER OUTPUT " + "="*18 + "\n")
    print(res_plan)
    Path("outputs/Plan.md").write_text(res_plan, encoding="utf-8")

    # ---- Market Analyst ----
    analyst = build_analyst()
    t_brief = market_brief_task(idea, planner_notes=res_plan, agent=analyst)
    res_brief = to_text(Crew(agents=[analyst], tasks=[t_brief],
                             process=Process.sequential, verbose=True).kickoff())
    print("\n" + "="*16 + " MARKET BRIEF OUTPUT " + "="*16 + "\n")
    print(res_brief)
    Path("outputs/MarketBrief.md").write_text(res_brief, encoding="utf-8")

    # ---- Product Designer (PRD) ----
    designer = build_designer()
    t_prd = prd_task(idea, market_brief_md=res_brief, agent=designer)
    res_prd = to_text(Crew(agents=[designer], tasks=[t_prd],
                           process=Process.sequential, verbose=True).kickoff())
    print("\n" + "="*20 + " PRD OUTPUT " + "="*20 + "\n")
    print(res_prd)
    Path("outputs/PRD.md").write_text(res_prd, encoding="utf-8")

    # ---- Page Builder (HTML) ----
    page_builder = build_page_builder()
    t_lp = landing_page_task(idea, copy_blocks_md=res_prd, agent=page_builder)
    res_html = to_text(Crew(agents=[page_builder], tasks=[t_lp],
                            process=Process.sequential, verbose=True).kickoff())
    print("\n" + "="*18 + " LANDING HTML (first 60 lines) " + "="*18 + "\n")
    print("\n".join(res_html.splitlines()[:60]))
    Path("outputs/landing/index.html").write_text(res_html, encoding="utf-8")

    print("\nSaved files:")
    print("  - outputs/Plan.md")
    print("  - outputs/MarketBrief.md")
    print("  - outputs/PRD.md")
    print("  - outputs/landing/index.html")

if __name__ == "__main__":
    main()
