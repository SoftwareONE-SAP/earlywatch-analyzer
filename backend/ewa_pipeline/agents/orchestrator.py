"""
LangGraph coordinator-worker graph for EWA analysis.

Topology:
    START → planner → [Send(domain_analyst) × N in parallel]
          → cross_reference → synthesize → END

planner         (orchestrator deployment) Reads the tree and produces SectionTasks.
domain_analyst  (specialist deployment)   Runs one analysis per selected section.
cross_reference (orchestrator deployment) Correlates findings across sections.
synthesize      (orchestrator deployment) Produces the executive summary and priorities.
"""

from __future__ import annotations

import json
import operator
from typing import Annotated, Any, TypedDict

from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, START, END
from langgraph.types import Send

from ewa_pipeline.config import Config
from ewa_pipeline.models import get_orchestrator_model, get_subagent_model, get_cross_ref_model
from ewa_pipeline.tracking.cost_tracker import CostTracker
from ewa_pipeline.report.schemas import (
    DomainAnalysis, CrossReferenceList, OrchestratorPlan, SynthesisResult,
)
from .skill_loader import SkillRegistry
from .prompts import (
    ORCHESTRATOR_SYSTEM_PROMPT,
    ORCHESTRATOR_PLANNING_PROMPT,
    DOMAIN_ANALYST_PROMPT,
    CROSS_REFERENCE_PROMPT,
)


# ── State ─────────────────────────────────────────────────────────────────────

class EwaAnalysisState(TypedDict):
    # Inputs — set once before the graph runs
    tree_summary: str
    sections_available: list[dict]       # [{id, title, summary}] — for planner
    sections_content: dict[str, str]     # section_id to source content
    skills_catalog: str

    # After planner node
    section_tasks: list[dict]            # [{section_id, section_title, analysis_focus}]
    planning_notes: str

    # Accumulated from parallel domain_analyst nodes
    domain_analyses: Annotated[list[DomainAnalysis], operator.add]
    failed_sections: Annotated[list[str], operator.add]

    # After cross_reference node
    cross_references: list

    # After synthesize node
    executive_summary: str
    overall_system_health: str
    top_5_priority_actions: list[str]


# ── Helpers ───────────────────────────────────────────────────────────────────

def _usage_details(meta: Any, key: str, *detail_keys: str) -> int:
    if isinstance(meta, dict):
        details = meta.get(key) or {}
        if isinstance(details, dict):
            return int(next((details.get(k) for k in detail_keys if details.get(k)), 0) or 0)
        return 0

    details = getattr(meta, key, None)
    if details is None:
        return 0
    if isinstance(details, dict):
        return int(next((details.get(k) for k in detail_keys if details.get(k)), 0) or 0)
    return int(next((getattr(details, k, 0) for k in detail_keys if getattr(details, k, 0)), 0) or 0)


def _usage_value(meta: Any, key: str) -> int:
    if isinstance(meta, dict):
        return int(meta.get(key, 0) or 0)
    return int(getattr(meta, key, 0) or 0)


def _tokens(raw: Any) -> tuple[int, int, int, int]:
    meta = getattr(raw, "usage_metadata", None) or {}
    return (
        _usage_value(meta, "input_tokens"),
        _usage_value(meta, "output_tokens"),
        _usage_details(meta, "input_token_details", "cache_read"),
        _usage_details(
            meta,
            "input_token_details",
            "cache_write_tokens",
            "cache_write",
            "cache_creation",
        ),
    )


def _derive_health(analyses: list[DomainAnalysis]) -> str:
    healths = {da.overall_health for da in analyses}
    if "Critical" in healths:
        return "Critical"
    if "Warning" in healths:
        return "Warning"
    return "Healthy"


def _normalise_finding_ids(
    analysis: DomainAnalysis,
    *,
    section_id: str | None = None,
    section_title: str | None = None,
) -> DomainAnalysis:
    """Use trusted section metadata and globally unambiguous finding IDs."""
    trusted_id = str(section_id or analysis.section_id).strip()
    findings = [
        finding.model_copy(update={"id": f"{trusted_id}-F{index:03d}"})
        for index, finding in enumerate(analysis.findings, start=1)
    ]
    return analysis.model_copy(
        update={
            "section_id": trusted_id,
            "section_title": section_title or analysis.section_title,
            "findings": findings,
        }
    )


def _normalise_section_tasks(
    tasks: list[dict],
    sections_available: list[dict],
) -> list[dict]:
    """Drop unknown or duplicate planner IDs and trust indexed section titles."""
    title_lookup = {
        str(section["id"]): section["title"]
        for section in sections_available
    }
    normalized: list[dict] = []
    seen: set[str] = set()
    for task in tasks:
        raw_id = task.get("section_id", "")
        section_id = str(raw_id).strip().strip("[]'\"").strip()
        if section_id in seen or section_id not in title_lookup:
            continue
        seen.add(section_id)
        normalized.append(
            {
                **task,
                "section_id": section_id,
                "section_title": title_lookup[section_id],
            }
        )
    return normalized


# ── Graph factory ─────────────────────────────────────────────────────────────

def build_ewa_graph(
    config: Config,
    cost_tracker: CostTracker,
    skill_registry: SkillRegistry,
):
    """
    Compile and return the LangGraph EWA analysis graph.

    Nodes are closures — they capture config, cost_tracker, and LLM chains.
    Call graph.stream(initial_state) to run with streaming event output.
    """
    specialist_deployment = config.azure_openai.deployments.specialist
    orchestrator_deployment = config.azure_openai.deployments.orchestrator

    planner_chain = get_orchestrator_model(config).with_structured_output(
        OrchestratorPlan, include_raw=True
    )
    domain_chain = get_subagent_model(config).with_structured_output(
        DomainAnalysis, include_raw=True
    )
    xref_chain = get_cross_ref_model(config).with_structured_output(
        CrossReferenceList, include_raw=True
    )
    synth_chain = get_orchestrator_model(config).with_structured_output(
        SynthesisResult, include_raw=True
    )

    # ── Node: planner ────────────────────────────────────────────────────────

    def planner(state: EwaAnalysisState) -> dict:
        """
        Orchestrator LLM reads the tree and produces a prioritised SectionTask list.
        Each task carries an analysis_focus hint that guides the domain analyst.
        """
        sections_text = "\n".join(
            f"  id={s['id']} | {s['title']}: {s.get('summary', '')[:120]}"
            for s in state["sections_available"]
        )
        prompt = ORCHESTRATOR_PLANNING_PROMPT.format(
            tree_summary=state["tree_summary"],
            sections=sections_text,
            skills_catalog=state["skills_catalog"],
        )
        result = planner_chain.invoke(
            [SystemMessage(content=ORCHESTRATOR_SYSTEM_PROMPT), HumanMessage(content=prompt)]
        )
        inp, out, cached_inp, cache_write = _tokens(result.get("raw"))
        cost_tracker.record(
            "phase0_planning",
            orchestrator_deployment,
            inp,
            out,
            cached_input_tokens=cached_inp,
            cache_write_tokens=cache_write,
        )

        plan: OrchestratorPlan = result["parsed"]
        section_tasks = _normalise_section_tasks(
            [task.model_dump() for task in plan.tasks],
            state["sections_available"],
        )
        return {
            "section_tasks": section_tasks,
            "planning_notes": plan.planning_notes,
        }

    # ── Conditional edge: fan out sections to parallel domain analysts ────────

    def route_sections(state: EwaAnalysisState) -> list[Send] | str:
        """
        Dispatch each section task as a parallel Send to domain_analyst.
        Falls through to cross_reference directly if the planner produced no tasks.
        """
        if not state["section_tasks"]:
            return "cross_reference"

        normalized_tasks = _normalise_section_tasks(
            state["section_tasks"],
            state["sections_available"],
        )
        if not normalized_tasks:
            return "cross_reference"

        sends = []
        for task in normalized_tasks:
            sid = task["section_id"]
            sends.append(Send("domain_analyst", {
                "section_id": sid,
                "section_title": task["section_title"],
                "content": state["sections_content"].get(sid, ""),
                "skill_name": task.get("skill_name") or "ewa-analysis",
                "reference_ids": task.get("reference_ids") or [],
                "analysis_focus": task.get("analysis_focus", ""),
            }))
        return sends

    # ── Node: domain_analyst ─────────────────────────────────────────────────

    def domain_analyst(task: dict) -> dict:
        """
        Analyse a single section. Runs in parallel — one invocation per Send.
        Returns {"domain_analyses": [da]} which is accumulated via operator.add.
        """
        reference_ids = task.get("reference_ids") or []
        if not reference_ids:
            reference_ids = skill_registry.suggest_references(
                task.get("skill_name") or "ewa-analysis",
                " ".join(
                    [
                        task.get("section_title", ""),
                        task.get("analysis_focus", ""),
                        task.get("content", "")[:1200],
                    ]
                ),
            )
        skill_context = skill_registry.resolve_context(
            task.get("skill_name") or "ewa-analysis",
            reference_ids,
            fallback_text="No specific skill context was selected for this section.",
        )
        prompt = DOMAIN_ANALYST_PROMPT.format(
            section_title=task["section_title"],
            section_id=task["section_id"],
            content=task["content"],
            skill_context=skill_context,
            analysis_focus=task["analysis_focus"],
        )
        try:
            result = domain_chain.invoke([HumanMessage(content=prompt)])
            inp, out, cached_inp, cache_write = _tokens(result.get("raw"))
            cost_tracker.record(
                "phase1_domain_analysis",
                specialist_deployment,
                inp,
                out,
                cached_input_tokens=cached_inp,
                cache_write_tokens=cache_write,
            )
            da = _normalise_finding_ids(
                result["parsed"],
                section_id=task["section_id"],
                section_title=task["section_title"],
            )
            return {"domain_analyses": [da]}
        except Exception as exc:
            return {
                "domain_analyses": [],
                "failed_sections": [
                    f"{task['section_id']} ({task['section_title']}): {exc}"
                ],
            }

    # ── Node: cross_reference ────────────────────────────────────────────────

    def cross_reference(state: EwaAnalysisState) -> dict:
        all_findings = {
            da.section_id: da.model_dump()
            for da in state["domain_analyses"]
        }
        prompt = CROSS_REFERENCE_PROMPT.format(
            all_findings=json.dumps(all_findings, indent=2)
        )
        try:
            result = xref_chain.invoke([HumanMessage(content=prompt)])
            inp, out, cached_inp, cache_write = _tokens(result.get("raw"))
            cost_tracker.record(
                "phase2_cross_reference",
                orchestrator_deployment,
                inp,
                out,
                cached_input_tokens=cached_inp,
                cache_write_tokens=cache_write,
            )
            xref_list: CrossReferenceList = result["parsed"]
            return {"cross_references": xref_list.items}
        except Exception:
            return {"cross_references": []}

    # ── Node: synthesize ─────────────────────────────────────────────────────

    def synthesize(state: EwaAnalysisState) -> dict:
        all_findings_text = json.dumps(
            [da.model_dump() for da in state["domain_analyses"]], indent=2
        )
        cross_refs_text = json.dumps(
            [xr.model_dump() if hasattr(xr, "model_dump") else xr
             for xr in state["cross_references"]],
            indent=2,
        )
        prompt = f"""You have completed analysis of all sections in an SAP EWA report.

Tree structure:
{state['tree_summary'][:3000]}

All domain findings:
{all_findings_text}

Cross-domain correlations:
{cross_refs_text}

Write the final synthesis:
- overall_system_health: Critical if ANY domain is Critical; Warning if ANY domain is Warning; else Healthy
- top_5_priority_actions: ordered by urgency x impact, referencing specific findings and SAP transactions
- executive_summary: 3-5 paragraphs covering system overview, critical/high findings, key risks, priorities
  Use specific numbers, finding IDs, and SAP transactions — no vague language.
"""
        try:
            result = synth_chain.invoke(
                [SystemMessage(content=ORCHESTRATOR_SYSTEM_PROMPT), HumanMessage(content=prompt)]
            )
            inp, out, cached_inp, cache_write = _tokens(result.get("raw"))
            cost_tracker.record(
                "phase2_synthesis",
                orchestrator_deployment,
                inp,
                out,
                cached_input_tokens=cached_inp,
                cache_write_tokens=cache_write,
            )
            synthesis: SynthesisResult = result["parsed"]
            return {
                "executive_summary": synthesis.executive_summary,
                "overall_system_health": synthesis.overall_system_health,
                "top_5_priority_actions": synthesis.top_5_priority_actions,
            }
        except Exception:
            return {
                "executive_summary": "Synthesis unavailable.",
                "overall_system_health": _derive_health(state["domain_analyses"]),
                "top_5_priority_actions": [],
            }

    # ── Compile ───────────────────────────────────────────────────────────────

    builder = StateGraph(EwaAnalysisState)
    builder.add_node("planner", planner)
    builder.add_node("domain_analyst", domain_analyst)
    builder.add_node("cross_reference", cross_reference)
    builder.add_node("synthesize", synthesize)

    builder.add_edge(START, "planner")
    builder.add_conditional_edges(
        "planner", route_sections, ["domain_analyst", "cross_reference"]
    )
    builder.add_edge("domain_analyst", "cross_reference")
    builder.add_edge("cross_reference", "synthesize")
    builder.add_edge("synthesize", END)

    return builder.compile()
