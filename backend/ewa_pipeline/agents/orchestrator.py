"""
LangGraph coordinator-worker graph for EWA analysis.

Topology:
    START → planner → [Send(domain_analyst) × N in parallel]
          → cross_reference → synthesize → END

planner         (orchestrator deployment) Reads the tree and produces SectionTasks.
domain_analyst  (specialist deployment)   Reviews one bounded group per invocation.
cross_reference (cross-reference deployment) Correlates findings across sections.
synthesize      (synthesis deployment) Produces the executive summary and priorities.
"""

from __future__ import annotations

import html
import json
import operator
import re
from typing import Annotated, Any, NotRequired, TypedDict

from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, START, END
from langgraph.types import Send

from ewa_pipeline.config import Config
from ewa_pipeline.models import (
    get_orchestrator_model, get_subagent_model, get_cross_ref_model, get_synthesis_model, structured,
)
from ewa_pipeline.tracking.cost_tracker import CostTracker
from ewa_pipeline.report.schemas import (
    AnalysisTaskRecord, DomainAnalysis, GroupedDomainAnalysis,
    CrossReferenceList, OrchestratorPlan, SynthesisResult,
)
from .skill_loader import SkillRegistry
from .planning import validate_plan, parent_context, planning_catalogue
from .prompts import (
    ORCHESTRATOR_SYSTEM_PROMPT,
    ORCHESTRATOR_PLANNING_PROMPT,
    DOMAIN_ANALYST_PROMPT,
    GROUPED_DOMAIN_ANALYST_PROMPT,
    CROSS_REFERENCE_PROMPT,
)


# ── State ─────────────────────────────────────────────────────────────────────

class EwaAnalysisState(TypedDict):
    # Inputs — set once before the graph runs
    tree_summary: str
    sections_available: list[dict]       # source IDs, hierarchy, summaries, sizes
    sections_content: dict[str, str]     # section_id to source content
    context_sections: dict[str, str]
    skills_catalog: str
    system_profile: NotRequired[str]     # short system ID card text for analyst prompts

    # After planner node
    section_tasks: list[dict]            # grouped source IDs, budgets, context
    planning_notes: str
    analysis_tasks: list[AnalysisTaskRecord]

    # Accumulated from parallel domain_analyst nodes
    domain_analyses: Annotated[list[DomainAnalysis], operator.add]
    failed_sections: Annotated[list[dict], operator.add]

    # After cross_reference node
    cross_references: list
    correlation_failed: bool

    # After synthesize node
    executive_summary: str
    overall_system_health: str
    top_5_priority_actions: list[str]
    synthesis_failed: bool


# ── Helpers ───────────────────────────────────────────────────────────────────

# Finding fields the cross-reference and synthesis calls do not need (saves input tokens).
_LATER_CALL_EXCLUDED_FINDING_FIELDS = {"confidence_reason", "to_confirm", "due_date"}


def _dump_for_later_calls(analysis: DomainAnalysis) -> dict:
    return analysis.model_dump(
        exclude={"findings": {"__all__": _LATER_CALL_EXCLUDED_FINDING_FIELDS}}
    )

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


_ROW = r"<tr(?:\s[^>]*)?>(.*?)</tr\s*>"
_TR_RE = re.compile(r"\s*(?:" + _ROW + r"\s*)+", re.IGNORECASE | re.DOTALL)
_ROW_RE = re.compile(_ROW, re.IGNORECASE | re.DOTALL)
_CELL_RE = re.compile(r"<t[dh](?:\s[^>]*)?>(.*?)</t[dh]\s*>", re.IGNORECASE | re.DOTALL)
_TAG_RE = re.compile(r"</?[A-Za-z][^<>]*>")
_ID_PREFIX_RE = re.compile(r"^\s*\d{4}\s*[,:]\s*")
_IMAGE_LINE_RE = re.compile(r"^\s*(?:[^:]*:\s*)?[\"'“”]?\[IMAGE\][\"'“”]?\s*$")


def clean_evidence(text: str) -> str:
    """Make finding evidence readable: no HTML tags, source-ID prefixes or [IMAGE] lines."""
    if not text:
        return text

    def _rows(match: re.Match) -> str:
        lines = []
        for row in _ROW_RE.findall(match.group(0)):
            cells = [_TAG_RE.sub("", c).strip() for c in _CELL_RE.findall(row)]
            lines.append(" | ".join(cells))
        return "\n" + "\n".join(lines) + "\n"

    text = _TR_RE.sub(_rows, text)
    text = _TAG_RE.sub("", text)
    text = html.unescape(text)

    lines: list[str] = []
    for raw in text.splitlines():
        line = _ID_PREFIX_RE.sub("", raw.rstrip(), count=1).rstrip()
        if line.strip().strip("\"'").strip() == "[IMAGE]" or _IMAGE_LINE_RE.match(line):
            continue
        if not line.strip() and (not lines or not lines[-1]):
            continue
        lines.append(line)
    while lines and not lines[-1]:
        lines.pop()
    return "\n".join(lines)


def _normalise_finding_ids(
    analysis: DomainAnalysis,
    *,
    section_id: str | None = None,
    section_title: str | None = None,
) -> DomainAnalysis:
    """Use trusted section metadata and globally unambiguous finding IDs."""
    trusted_id = str(section_id or analysis.section_id).strip()
    findings = [
        finding.model_copy(
            update={
                "id": f"{trusted_id}-F{index:03d}",
                "evidence": clean_evidence(finding.evidence),
            }
        )
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
    cross_reference_deployment, _ = config.model_settings("cross_reference")
    synthesis_deployment, _ = config.model_settings("synthesis")

    planner_chain = structured(get_orchestrator_model(config), OrchestratorPlan)
    specialist_model = get_subagent_model(config)
    domain_chain = structured(specialist_model, DomainAnalysis)
    grouped_chain = structured(specialist_model, GroupedDomainAnalysis)
    xref_chain = structured(get_cross_ref_model(config), CrossReferenceList)
    synth_chain = structured(get_synthesis_model(config), SynthesisResult)

    # ── Node: planner ────────────────────────────────────────────────────────

    def planner(state: EwaAnalysisState) -> dict:
        prompt = ORCHESTRATOR_PLANNING_PROMPT.format(
            sections=json.dumps(planning_catalogue(state["sections_available"], state["context_sections"])),
            skills_catalog=state["skills_catalog"],
            max_task_sections=config.max_task_sections,
            max_task_content_chars=config.max_task_content_chars,
        )
        plan = None
        try:
            result = planner_chain.invoke(
                [SystemMessage(content=ORCHESTRATOR_SYSTEM_PROMPT), HumanMessage(content=prompt)]
            )
            inp, out, cached, cache_write = _tokens(result.get("raw"))
            cost_tracker.record("phase0_planning", orchestrator_deployment, inp, out,
                                cached_input_tokens=cached, cache_write_tokens=cache_write)
            if isinstance(result.get("parsed"), OrchestratorPlan):
                plan = result["parsed"]
        except Exception:
            # Hierarchy fallback still owns every eligible section exactly once.
            pass
        tasks, _, notes = validate_plan(plan, state["sections_available"], config)
        records = []
        for task in tasks:
            context, context_ids = parent_context(task["section_ids"], state["sections_available"],
                state["context_sections"], config.max_parent_context_chars)
            task["parent_context"] = context
            records.append(AnalysisTaskRecord(task_id=task["task_id"], title=task["section_title"],
                source_section_ids=task["section_ids"], context_section_ids=context_ids,
                source_content_chars=task["source_content_chars"], context_content_chars=len(context),
                origin=task["task_origin"], within_budget=not task["oversized"]))
        return {"section_tasks": tasks, "analysis_tasks": records,
                "planning_notes": " ".join([plan.planning_notes if plan else "", *notes]).strip()}

    def route_sections(state: EwaAnalysisState) -> list[Send] | str:
        if not state["section_tasks"]:
            return "cross_reference"
        lookup = {s["id"]: s for s in state["sections_available"]}
        profile = state.get("system_profile", "")
        return [Send("domain_analyst", {**task, "system_profile": profile, "sources": [
            {"id": sid, "title": lookup[sid]["title"], "content": state["sections_content"][sid]}
            for sid in task["section_ids"]]}) for task in state["section_tasks"]]

    def domain_analyst(task: dict) -> dict:
        """One bounded invocation; preserve each source's identity and full content."""
        sources = task["sources"]
        profile_text = task.get("system_profile") or "Not available."
        references = task.get("reference_ids") or skill_registry.suggest_references(
            task["skill_name"], " ".join([task["section_title"], task["analysis_focus"],
                *[s["title"] + " " + s["content"][:100] for s in sources]]))
        context = skill_registry.resolve_context(task["skill_name"], references,
            fallback_text="No specific skill context was selected for this group.")
        reason, parsed = "", None
        if task["oversized"]:
            reason = "Individual source exceeds configured task budget; no content truncated or model call made."
        else:
            if len(sources) == 1:
                source = sources[0]
                prompt = DOMAIN_ANALYST_PROMPT.format(section_title=source["title"], section_id=source["id"],
                    content=source["content"], skill_context=context, analysis_focus=task["analysis_focus"],
                    system_profile=profile_text)
                chain = domain_chain
            else:
                source_text = "\n\n".join(
                    f"Source Section ID: {s['id']}\nSource title: {s['title']}\n{s['content']}" for s in sources)
                prompt = GROUPED_DOMAIN_ANALYST_PROMPT.format(section_title=task["section_title"],
                    section_ids=", ".join(task["section_ids"]), content=source_text,
                    skill_context=context, analysis_focus=task["analysis_focus"],
                    system_profile=profile_text)
                chain = grouped_chain
            if task["parent_context"]:
                prompt += "\n\nSupplementary parent context (excerpts; not owned source sections):\n" + task["parent_context"]
            try:
                result = chain.invoke([HumanMessage(content=prompt)])
                inp, out, cached, cache_write = _tokens(result.get("raw"))
                # Charge once per request, even when it owns multiple sections.
                cost_tracker.record("phase1_domain_analysis", specialist_deployment, inp, out,
                                    cached_input_tokens=cached, cache_write_tokens=cache_write)
                parsed = result.get("parsed")
            except Exception:
                reason = "Model call failed; source content and provider details omitted."
        if isinstance(parsed, GroupedDomainAnalysis) and len(sources) > 1:
            returned = parsed.analyses
        elif isinstance(parsed, DomainAnalysis) and len(sources) == 1:
            returned = [parsed]
        else:
            returned = []
            reason = reason or "Model returned no parsable analysis."
        ids = [str(analysis.section_id).strip("[]'\" ") for analysis in returned]
        if any(sid not in task["section_ids"] for sid in ids) or len(ids) != len(set(ids)):
            reason = "Model returned unexpected or duplicate source identities."
        by_id = dict(zip(ids, returned))
        analyses, failures = [], []
        for source in sources:
            sid = source["id"]
            if reason or sid not in by_id:
                failures.append({"section_id": sid, "section_title": source["title"],
                                 "reason": reason or "Group response omitted this source section."})
            else:
                analyses.append(_normalise_finding_ids(by_id[sid], section_id=sid, section_title=source["title"]))
        return {"domain_analyses": analyses, "failed_sections": failures}

    def cross_reference(state: EwaAnalysisState) -> dict:
        if not state["domain_analyses"]:
            return {"cross_references": [], "correlation_failed": True}
        all_findings = {
            da.section_id: _dump_for_later_calls(da)
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
                cross_reference_deployment,
                inp,
                out,
                cached_input_tokens=cached_inp,
                cache_write_tokens=cache_write,
            )
            xref_list = result.get("parsed")
            if not isinstance(xref_list, CrossReferenceList):
                raise ValueError("Cross-reference response could not be parsed")
            valid_ids = {finding.id for analysis in state["domain_analyses"] for finding in analysis.findings}
            valid = [item for item in xref_list.items
                     if item.related_findings and all(rid in valid_ids for rid in item.related_findings)]
            return {"cross_references": valid, "correlation_failed": len(valid) != len(xref_list.items)}
        except Exception:
            return {"cross_references": [], "correlation_failed": True}

    # ── Node: synthesize ─────────────────────────────────────────────────────

    def synthesize(state: EwaAnalysisState) -> dict:
        if not state["domain_analyses"]:
            return {"executive_summary": "No section analysis succeeded.", "overall_system_health": "Unknown",
                    "top_5_priority_actions": [], "synthesis_failed": True}
        all_findings_text = json.dumps(
            [_dump_for_later_calls(da) for da in state["domain_analyses"]], indent=2
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
                synthesis_deployment,
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
                "overall_system_health": "Unknown",
                "top_5_priority_actions": [],
                "synthesis_failed": True,
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
