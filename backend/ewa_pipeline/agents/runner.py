from __future__ import annotations

from pathlib import Path

from rich.console import Console

from ewa_pipeline.config import Config
from ewa_pipeline.indexer.tree_navigator import TreeNode, get_node_content, tree_to_summary
from ewa_pipeline.tracking.cost_tracker import CostTracker
from ewa_pipeline.tracking.token_tracker import TokenUsage
from ewa_pipeline.report.schemas import AnalysisResult, DomainAnalysis, SectionCoverage
from ewa_pipeline.services.progress import ProgressCallback, ProgressReporter
from .orchestrator import EwaAnalysisState, build_ewa_graph
from .provenance import enrich_domain_analysis_provenance
from .skill_loader import SkillRegistry
from .planning import prepare_sections

console = Console()


class AnalysisFailedError(RuntimeError):
    """No source section was analysed successfully."""


# Annotated[list, operator.add] fields — merged by appending, not overwriting
_ACCUMULATOR_KEYS = frozenset({"domain_analyses", "failed_sections"})


def run_analysis(
    config: Config,
    tree: dict,
    pages: dict[int, str],
    sections: list[TreeNode],
    skills_dir: Path,
    cost_tracker: CostTracker,
    verbose: bool = False,
    progress_callback: ProgressCallback | None = None,
) -> AnalysisResult:
    """
    Run the full LangGraph EWA analysis pipeline.

    Graph topology:
        planner → [domain_analyst × N in parallel] → cross_reference → synthesize

    State is accumulated during a single graph.stream() pass — no double invocation.
    """
    reporter = ProgressReporter(progress_callback)

    # ── Build initial state ───────────────────────────────────────────────────

    skill_registry = SkillRegistry.from_dir(skills_dir)
    skills_catalog = skill_registry.catalog_text()
    sections_content = {
        node.id: get_node_content(pages, node)
        for node in sections
    }
    eligible_sections = [node for node in sections if sections_content[node.id].strip()]
    if not eligible_sections:
        raise AnalysisFailedError("No text-bearing source sections are available for analysis.")
    sections_available, context_sections = prepare_sections(tree, eligible_sections, sections_content)

    initial_state: EwaAnalysisState = {
        "tree_summary": tree_to_summary(tree),
        "sections_available": sections_available,
        "sections_content": sections_content,
        "context_sections": context_sections,
        "skills_catalog": skills_catalog,
        "section_tasks": [],
        "planning_notes": "",
        "analysis_tasks": [],
        "domain_analyses": [],
        "failed_sections": [],
        "cross_references": [],
        "correlation_failed": False,
        "executive_summary": "",
        "overall_system_health": "Healthy",
        "top_5_priority_actions": [],
        "synthesis_failed": False,
    }

    if verbose:
        console.print(f"  Tree summary:\n{initial_state['tree_summary'][:800]}")
        console.print(f"  Skill catalog loaded: {len(skills_catalog)} chars")

    # ── Stream graph, report progress, accumulate final state ─────────────────

    graph = build_ewa_graph(config, cost_tracker, skill_registry)
    total_sections = len(eligible_sections)
    analyzed_count = 0
    completed_tasks = 0

    # We accumulate state deltas ourselves so we don't need a second invoke() call.
    # Annotated[list, operator.add] fields are appended; all others are overwritten.
    accumulated: dict = dict(initial_state)

    reporter.emit(
        "planning",
        "running",
        "Orchestrator planning analysis",
        detail=f"{total_sections} sections available",
    )

    for chunk in graph.stream(
        initial_state, config={"max_concurrency": config.max_concurrency}, stream_mode="updates"
    ):
        for node_name, update in chunk.items():

            # ── Accumulate state ─────────────────────────────────────────────
            for key, value in update.items():
                if key in _ACCUMULATOR_KEYS:
                    accumulated[key] = accumulated.get(key, []) + (
                        value if isinstance(value, list) else []
                    )
                else:
                    accumulated[key] = value

            # ── Progress events ──────────────────────────────────────────────
            if node_name == "planner":
                num_tasks = len(update.get("section_tasks", []))
                notes = update.get("planning_notes", "")
                reporter.emit(
                    "planning",
                    "completed",
                    "Analysis plan ready",
                    detail=f"{num_tasks} tasks covering {total_sections} source sections"
                    + (f" — {notes}" if notes else ""),
                )
                reporter.emit(
                    "analyzing_sections",
                    "running",
                    "Analyzing sections",
                    detail=f"0 / {num_tasks}",
                    current=0,
                    total=num_tasks or 1,
                )
                if verbose:
                    console.print(
                        f"  [cyan]Plan[/cyan]: {num_tasks} sections"
                        + (f" — {notes}" if notes else "")
                    )

            elif node_name == "domain_analyst":
                new_das: list[DomainAnalysis] = update.get("domain_analyses", [])
                new_failures: list[dict] = update.get("failed_sections", [])
                analyzed_count += len(new_das) + len(new_failures)
                completed_tasks += 1
                planned = len(accumulated.get("section_tasks", [])) or total_sections

                for da in new_das:
                    if verbose:
                        color = {"Critical": "red", "Warning": "yellow", "Healthy": "green"}.get(
                            da.overall_health, "white"
                        )
                        console.print(
                            f"  [{color}]{da.overall_health}[/{color}]"
                            f" {da.section_title} — {len(da.findings)} finding(s)"
                        )
                for fail in new_failures:
                    console.print(f"  [yellow]Warning[/yellow]: {fail['section_id']}: {fail['reason']}")

                reporter.emit(
                    "analyzing_sections",
                    "running",
                    "Analyzing sections",
                    detail=f"{completed_tasks} / {planned} tasks; {analyzed_count} / {total_sections} sources",
                    current=completed_tasks,
                    total=planned,
                )

            elif node_name == "cross_reference":
                xrefs = update.get("cross_references", [])
                reporter.emit(
                    "analyzing_sections",
                    "completed",
                    "Section analysis complete",
                    detail=f"{analyzed_count} sections processed",
                    current=analyzed_count,
                    total=analyzed_count or 1,
                )
                reporter.emit(
                    "correlating_findings",
                    "completed",
                    "Cross-referencing complete",
                    detail=f"{len(xrefs)} correlations",
                )

            elif node_name == "synthesize":
                reporter.emit(
                    "synthesizing",
                    "completed",
                    "Synthesis complete",
                    detail=update.get("overall_system_health", ""),
                )

    # ── Build AnalysisResult from accumulated state ───────────────────────────

    domain_analyses: list[DomainAnalysis] = [
        enrich_domain_analysis_provenance(analysis)
        for analysis in accumulated["domain_analyses"]
    ]
    cross_references = accumulated["cross_references"]
    if not domain_analyses:
        raise AnalysisFailedError("No source sections were analysed successfully; check task budgets and model configuration.")
    by_id = {analysis.section_id: analysis for analysis in domain_analyses}
    failed = {failure["section_id"]: failure["reason"] for failure in accumulated["failed_sections"]}
    task_ids = {sid: task.task_id for task in accumulated["analysis_tasks"] for sid in task.source_section_ids}
    coverage = [SectionCoverage(section_id=node.id, section_title=node.title,
                analysis_task_id=task_ids.get(node.id, ""),
                status="analyzed" if node.id in by_id else "failed",
                reason="" if node.id in by_id else failed.get(node.id, "Source produced no result."))
                for node in eligible_sections]
    coverage += [SectionCoverage(section_id=node.id, section_title=node.title, status="skipped",
                                reason="Section contains no text content.")
                 for node in sections if node not in eligible_sections]
    warnings = [f"Section {sid}: {reason}" for sid, reason in failed.items()]
    if accumulated["correlation_failed"]:
        warnings.append("Cross-reference analysis was incomplete.")
    if accumulated["synthesis_failed"]:
        warnings.append("Executive synthesis was unavailable.")
    degraded = any(item.status == "failed" for item in coverage) or bool(warnings)
    health = accumulated["overall_system_health"]
    ranks = {"Healthy": 0, "Warning": 1, "Critical": 2}
    for analysis in domain_analyses:
        candidates = [analysis.overall_health]
        if any(finding.severity == "Critical" for finding in analysis.findings):
            candidates.append("Critical")
        elif any(finding.severity == "High" for finding in analysis.findings):
            candidates.append("Warning")
        health = max([health, *candidates], key=lambda value: ranks.get(value, 0))
    if degraded:
        health = "Unknown"

    p0 = cost_tracker._entries.get("phase0_planning")
    p1 = cost_tracker._entries.get("phase1_domain_analysis")
    p2a = cost_tracker._entries.get("phase2_cross_reference")
    p2b = cost_tracker._entries.get("phase2_synthesis")
    token_usage = TokenUsage(
        phase0_model=(p0.model if p0 else ""),
        phase0_input_tokens=(p0.input_tokens if p0 else 0),
        phase0_cached_input_tokens=(p0.cached_input_tokens if p0 else 0),
        phase0_cache_write_tokens=(p0.cache_write_tokens if p0 else 0),
        phase0_output_tokens=(p0.output_tokens if p0 else 0),
        phase1_model=(p1.model if p1 else ""),
        phase1_input_tokens=(p1.input_tokens if p1 else 0),
        phase1_cached_input_tokens=(p1.cached_input_tokens if p1 else 0),
        phase1_cache_write_tokens=(p1.cache_write_tokens if p1 else 0),
        phase1_output_tokens=(p1.output_tokens if p1 else 0),
        phase2_model=((p2a or p2b).model if (p2a or p2b) else ""),
        phase2_input_tokens=(
            (p2a.input_tokens if p2a else 0) + (p2b.input_tokens if p2b else 0)
        ),
        phase2_cached_input_tokens=(
            (p2a.cached_input_tokens if p2a else 0) + (p2b.cached_input_tokens if p2b else 0)
        ),
        phase2_cache_write_tokens=(
            (p2a.cache_write_tokens if p2a else 0)
            + (p2b.cache_write_tokens if p2b else 0)
        ),
        phase2_output_tokens=(
            (p2a.output_tokens if p2a else 0) + (p2b.output_tokens if p2b else 0)
        ),
    )

    return AnalysisResult(
        domain_analyses=domain_analyses,
        cross_references=cross_references,
        executive_summary=accumulated["executive_summary"],
        overall_system_health=health,
        top_5_priority_actions=accumulated["top_5_priority_actions"],
        token_usage=token_usage,
        analysis_tasks=accumulated["analysis_tasks"],
        coverage=coverage,
        degraded=degraded,
        warnings=warnings,
    )
