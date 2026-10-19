from typing import Literal
from pydantic import BaseModel, Field
from ewa_pipeline.tracking.token_tracker import TokenUsage


class SectionPlanItem(BaseModel):
    section_ids: list[str]
    section_title: str
    analysis_focus: str
    skill_name: str | None = None
    reference_ids: list[str] = Field(default_factory=list)


class OrchestratorPlan(BaseModel):
    tasks: list[SectionPlanItem]
    planning_notes: str = ""


class Remediation(BaseModel):
    action: str
    sap_transactions: list[str]
    effort_estimate: Literal["Low", "Medium", "High"]
    priority: Literal["Immediate", "Short-term", "Medium-term", "Long-term"]
    external_validation_required: bool = False
    validation_reason: str = "No external validation required."
    validation_query: str = ""
    allowed_sources: list[str] = Field(default_factory=list)


class Finding(BaseModel):
    id: str
    title: str
    severity: Literal["Critical", "High", "Medium", "Low"]
    description: str
    evidence: str
    impact: str
    remediation: Remediation


class DomainAnalysis(BaseModel):
    section_title: str
    section_id: str
    findings: list[Finding]
    overall_health: Literal["Critical", "Warning", "Healthy"]


class GroupedDomainAnalysis(BaseModel):
    """One shared-context request with a separately attributed result per source."""

    analyses: list[DomainAnalysis]


class AnalysisTaskRecord(BaseModel):
    task_id: str
    title: str
    source_section_ids: list[str]
    context_section_ids: list[str] = Field(default_factory=list)
    source_content_chars: int
    context_content_chars: int = 0
    origin: str
    within_budget: bool = True


class SectionCoverage(BaseModel):
    section_id: str
    section_title: str
    analysis_task_id: str = ""
    status: Literal["analyzed", "failed", "skipped"]
    reason: str = ""


class CrossReference(BaseModel):
    title: str
    related_findings: list[str]
    correlation_description: str
    combined_impact: str
    recommended_action: str


class CrossReferenceList(BaseModel):
    """Wrapper so with_structured_output can return a list of CrossReferences."""
    items: list[CrossReference]


class SynthesisResult(BaseModel):
    executive_summary: str
    overall_system_health: Literal["Critical", "Warning", "Healthy"]
    top_5_priority_actions: list[str]


class AnalysisResult(BaseModel):
    domain_analyses: list[DomainAnalysis]
    cross_references: list[CrossReference]
    executive_summary: str
    overall_system_health: Literal["Critical", "Warning", "Healthy", "Unknown"]
    top_5_priority_actions: list[str]
    token_usage: TokenUsage
    analysis_tasks: list[AnalysisTaskRecord] = Field(default_factory=list)
    coverage: list[SectionCoverage] = Field(default_factory=list)
    degraded: bool = False
    warnings: list[str] = Field(default_factory=list)
