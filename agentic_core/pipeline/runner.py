# pipeline/runner.py
from dotenv import load_dotenv
load_dotenv()

from pathlib import Path
from crewai import Crew, Process
from agents.planner import build_agent as build_planner, plan_task
from agents.market_analyst import build_agent as build_analyst, market_brief_task
from agents.designer import build_agent as build_designer, prd_task
from agents.page_builder import build_agent as build_page_builder, landing_page_task

def run(idea: str):
    # ensure folders exist
    Path("outputs/landing").mkdir(parents=True, exist_ok=True)

    # build agents
    planner = build_planner()
    analyst = build_analyst()
    designer = build_designer()
    page_builder = build_page_builder()

    # tasks (use context to pass outputs along), and write files
    t1 = plan_task(idea, agent=planner)
    t1.output_file = "outputs/Plan.md"

    t2 = market_brief_task(idea, planner_notes="", agent=analyst)
    t2.context = [t1]
    t2.output_file = "outputs/MarketBrief.md"

    t3 = prd_task(idea, market_brief_md="", agent=designer)
    t3.context = [t2]
    t3.output_file = "outputs/PRD.md"

    t4 = landing_page_task(idea, copy_blocks_md="", agent=page_builder)
    t4.context = [t3]
    t4.output_file = "outputs/landing/index.html"

    crew = Crew(
        agents=[planner, analyst, designer, page_builder],
        tasks=[t1, t2, t3, t4],
        process=Process.sequential,
        verbose=True,
    )
    crew.kickoff(inputs={"idea": idea})

    return {
        "plan": t1.output_file,
        "market_brief": t2.output_file,
        "prd": t3.output_file,
        "landing": t4.output_file,
    }

if __name__ == "__main__":
    import sys
    idea = " ".join(sys.argv[1:]) or "AI-powered resume tailor"
    print(run(idea))
