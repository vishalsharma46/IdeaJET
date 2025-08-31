# agents/page_builder.py
from crewai import Agent, Task

def build_agent() -> Agent:
    return Agent(
        role="Page Builder",
        goal=("Render a static, clean HTML landing page with headline, 3–5 bullets, "
              "and a simple 'Join waitlist' form (no frameworks)."),
        backstory=("Plain-HTML craftsman. Semantic tags, accessible markup, minimal inline styles."),
        allow_delegation=False,
        verbose=True,
    )

def landing_page_task(
    idea: str,
    copy_blocks_md: str = "",
    agent: Agent | None = None
) -> Task:
    agent = agent or build_agent()
    return Task(
        description=(
            f"Produce minimal static HTML for idea: `{idea}`.\n"
            "Use copy hints if provided (markdown below).\n"
            "=== COPY HINTS START ===\n"
            f"{copy_blocks_md}\n"
            "=== COPY HINTS END ===\n\n"
            "HTML requirements:\n"
            "- <head> with <title> and responsive <meta viewport>\n"
            "- <header> headline (h1)\n"
            "- 3–5 bullets (ul > li) explaining the value\n"
            "- A simple waitlist form: <form method=\"POST\" action=\"/waitlist\"> "
            "<input type=\"email\" name=\"email\" required> <button>Join waitlist</button>\n"
            "- Tiny inline CSS for readable typography, max-width container, spacing\n"
            "Return ONLY the full HTML string (no markdown)."
        ),
        agent=agent,
        expected_output="A single valid HTML document string ready to be written to index.html."
    )
