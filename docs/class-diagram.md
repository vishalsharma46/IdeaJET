classDiagram
  direction LR

  %% === App Layer ===
  class FastAPIApp {
    +run()
    +router: APIRouter
  }
  class LandingController {
    +get_index()
    +post_run(idea)
    +get_job(job_id)
    +post_waitlist(email, idea?)
  }
  class HealthController { +get_healthz() }

  FastAPIApp --> LandingController : routes
  FastAPIApp --> HealthController : routes

  %% === Services ===
  class JobService {
    +create_job(idea): Job
    +start_background_run(job_id)
    +get_status(job_id): JobStatusDTO
  }
  class WaitlistService {
    +add(email, idea?)
    +list()
  }
  class ArtifactService {
    +job_dir(job_id): Path
    +write_text(job_id, relpath, text)
    +write_json(job_id, relpath, obj)
    +exists(job_id, relpath): bool
  }

  LandingController --> JobService
  LandingController --> WaitlistService
  LandingController --> ArtifactService

  %% === Orchestration ===
  class CrewRunner {
    +run(job: Job): None
    -_run_planner(ctx)
    -_run_analyst(ctx)
    -_run_designer(ctx)
    -_run_page_builder(ctx)
  }
  class CrewFactory {
    +make_agents(): list~AgentBase~
    +make_tools(): list~ToolBase~
  }

  JobService --> CrewRunner
  CrewRunner --> CrewFactory

  %% === Agents ===
  class AgentBase {
    +name: str
    +run(context): StepResult
  }
  class PlannerAgent
  class MarketAnalystAgent
  class ProductDesignerAgent
  class PageBuilderAgent

  AgentBase <|-- PlannerAgent
  AgentBase <|-- MarketAnalystAgent
  AgentBase <|-- ProductDesignerAgent
  AgentBase <|-- PageBuilderAgent

  CrewRunner --> PlannerAgent
  CrewRunner --> MarketAnalystAgent
  CrewRunner --> ProductDesignerAgent
  CrewRunner --> PageBuilderAgent

  %% === Tools ===
  class ToolBase {
    +name: str
    +invoke(input): str
  }
  class WebSearchTool
  class WebScrapeTool
  class MarkdownWriterTool
  class StaticSiteTool
  class TemplateRenderer {
    +render(template, data): str
  }

  ToolBase <|-- WebSearchTool
  ToolBase <|-- WebScrapeTool
  ToolBase <|-- MarkdownWriterTool
  ToolBase <|-- StaticSiteTool
  StaticSiteTool --> TemplateRenderer

  PlannerAgent --> ToolBase : (optional)
  MarketAnalystAgent --> WebSearchTool
  MarketAnalystAgent --> WebScrapeTool
  ProductDesignerAgent --> MarkdownWriterTool
  PageBuilderAgent --> StaticSiteTool
  PageBuilderAgent --> ArtifactService

  %% === Persistence ===
  class JobRepo {
    +insert(Job): Job
    +update_status(id, status, error?)
    +get(id): Job
  }
  class RunLogRepo {
    +append(job_id, step, message)
    +list(job_id): list~RunLog~
  }
  class WaitlistRepo {
    +insert(email, idea?)
    +list(): list~WaitlistEntry~
  }

  JobService --> JobRepo
  JobService --> RunLogRepo
  WaitlistService --> WaitlistRepo

  %% === Domain Models ===
  class Job {
    +id: UUID
    +idea: str
    +status: JobStatus
    +created_at: datetime
    +updated_at: datetime
    +duration_ms: int
    +error: str?
  }
  class RunLog {
    +id: int
    +job_id: UUID
    +step: StepName
    +message: str
    +ts: datetime
  }
  class WaitlistEntry {
    +id: int
    +email: str
    +idea: str?
    +created_at: datetime
  }

  class CopyBlocks {
    +title: str
    +tagline: str
    +bullets: list~str~
    +cta_text: str
    +email_action: str
    +brand: str
  }
  class MarketBrief {
    +definition: str
    +tam: str
    +sam: str
    +som: str
    +competitors: list~Competitor~
    +sources: list~Source~
  }
  class PRD {
    +problem: str
    +target_users: str
    +jtbd: str
    +mvp_features: list~Feature~
    +acceptance_criteria: list~str~
    +risks: list~str~
  }
  class Competitor { +name; +url; +positioning; +notes }
  class Source { +title; +url; +note }
  class Feature { +name; +desc }

  CrewRunner --> ArtifactService
  CrewRunner --> JobRepo
  CrewRunner --> RunLogRepo
