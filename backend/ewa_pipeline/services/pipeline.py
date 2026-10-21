from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from rich.console import Console

from ewa_pipeline.agents.runner import run_analysis
from ewa_pipeline.config import Config
from ewa_pipeline.indexer.tree_navigator import get_analyzable_sections
from ewa_pipeline.report import excel_generator
from ewa_pipeline.report.schemas import AnalysisResult
from ewa_pipeline.tracking.cost_tracker import CostTracker
from .progress import ProgressCallback, ProgressReporter

console = Console()


@dataclass(slots=True)
class PipelineArtifacts:
    output_path: Path
    result_path: Path
    cost_path: Path
    tree_path: Path
    doc_name: str


def run_pipeline(
    *,
    config: Config,
    output_path: Path,
    input_path: Path | None = None,
    skip_index: bool = False,
    skip_analysis: bool = False,
    verbose: bool = False,
    skills_dir: Path | None = None,
    progress_callback: ProgressCallback | None = None,
) -> tuple[AnalysisResult, CostTracker, PipelineArtifacts]:
    if input_path is None:
        raise ValueError("Provide input_path.")

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    reporter = ProgressReporter(progress_callback)
    cost_tracker = CostTracker(pricing=config.pricing_dict())
    result_path = output_path.parent / f"{output_path.stem}_result.json"
    cost_path = output_path.parent / f"{output_path.stem}_cost.json"

    input_path = Path(input_path)
    input_suffix = input_path.suffix.lower()
    if input_suffix in {".htm", ".html"}:
        tree, pages, doc_name, tree_path, sections = _prepare_html_input(
            html_path=input_path,
            skip_index=skip_index,
            reporter=reporter,
        )
    elif input_suffix == ".doc":
        tree, pages, doc_name, tree_path, sections = _prepare_doc_input(
            doc_path=input_path,
            skip_index=skip_index,
            reporter=reporter,
        )
    else:
        raise ValueError(f"Unsupported input type: {input_suffix}")

    if skip_analysis and result_path.exists():
        reporter.emit(
            "analyzing_sections",
            "completed",
            "Reusing saved analysis",
            detail=result_path.name,
        )
        reporter.emit(
            "correlating_findings",
            "completed",
            "Reusing saved synthesis",
            detail=result_path.name,
        )
        result = AnalysisResult.model_validate_json(result_path.read_text(encoding="utf-8"))
    else:
        reporter.emit(
            "analyzing_sections",
            "running",
            "Analyzing sections",
            detail=f"{len(sections)} sections discovered",
            current=0,
            total=len(sections),
        )
        result = run_analysis(
            config=config,
            tree=tree,
            pages=pages,
            sections=sections,
            skills_dir=skills_dir or _default_skills_dir(),
            cost_tracker=cost_tracker,
            verbose=verbose,
            progress_callback=progress_callback,
        )
        result_path.write_text(result.model_dump_json(indent=2), encoding="utf-8")

    reporter.emit("generating_excel", "running", "Generating Excel workbook")
    excel_generator.generate(result, output_path, tree=tree)
    reporter.emit(
        "generating_excel",
        "completed",
        "Excel workbook ready",
        detail=output_path.name,
        percent=100,
    )

    cost_tracker.save(cost_path, document_name=doc_name)
    reporter.emit(
        "completed",
        "completed",
        "Analysis complete",
        detail=output_path.name,
        percent=100,
    )

    artifacts = PipelineArtifacts(
        output_path=output_path,
        result_path=result_path,
        cost_path=cost_path,
        tree_path=tree_path,
        doc_name=doc_name,
    )
    return result, cost_tracker, artifacts


def _default_skills_dir() -> Path:
    """Resolve skills directory relative to this package."""
    # backend/ewa_pipeline/services/pipeline.py → backend/skills
    backend_dir = Path(__file__).resolve().parent.parent.parent
    return backend_dir / "skills"


def _prepare_html_input(
    *,
    html_path: Path,
    skip_index: bool,
    reporter: ProgressReporter,
) -> tuple[dict, dict[int, str], str, Path, list]:
    """Prepare pipeline input from compact semantic HTML."""
    from ewa_pipeline.indexer.html_tree_builder import build_document_tree_from_html

    data_dir = html_path.parent
    tree_path = data_dir / f"{html_path.stem}_tree.json"

    reporter.emit(
        "normalizing_document",
        "completed",
        "Compact HTML loaded",
        detail=html_path.name,
    )

    if skip_index and tree_path.exists():
        reporter.emit("building_tree", "completed", "Reusing document structure", detail=tree_path.name)
        tree = json.loads(tree_path.read_text(encoding="utf-8"))
    else:
        reporter.emit("building_tree", "running", "Building HTML document structure", detail=html_path.name)
        tree = build_document_tree_from_html(html_path, data_dir)
        reporter.emit("building_tree", "completed", "Document structure ready", detail=tree_path.name)

    sections = get_analyzable_sections(tree)
    reporter.emit(
        "discovering_sections",
        "completed",
        "Sections discovered",
        detail=f"{len(sections)} sections ready",
        current=len(sections),
        total=len(sections) or 1,
    )
    return tree, {}, html_path.stem, tree_path, sections


def _prepare_doc_input(
    *,
    doc_path: Path,
    skip_index: bool,
    reporter: ProgressReporter,
) -> tuple[dict, dict[int, str], str, Path, list]:
    """Convert Word/Word XML to compact HTML, then prepare HTML input."""
    from converters.compact_html_converter import convert_html_to_compact_html
    from converters.doc_html_converter import convert_doc_to_html

    data_dir = doc_path.parent
    compact_path = data_dir / f"{doc_path.stem}.compact.html"
    reporter.emit("normalizing_document", "running", "Converting Word document to HTML", detail=doc_path.name)
    if not (skip_index and compact_path.exists()):
        html_path = convert_doc_to_html(
            doc_path,
            data_dir / f"{doc_path.stem}_html",
        )
        convert_html_to_compact_html(html_path, compact_path)
    reporter.emit("normalizing_document", "completed", "Compact HTML ready", detail=compact_path.name)
    return _prepare_html_input(html_path=compact_path, skip_index=skip_index, reporter=reporter)


