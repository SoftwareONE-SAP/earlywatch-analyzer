"""End-to-end conversion: Word .doc/.docx -> HTML (LibreOffice) -> Markdown."""

from __future__ import annotations

import logging
import re
import shutil
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from converters.doc_html_converter import convert_doc_to_html, discover_companion_dirs
from converters.html_markdown_converter import convert_html_to_markdown
from converters.word_com_html_converter import detect_word_document_kind

logger = logging.getLogger(__name__)

ICON_PATTERN = re.compile(
    r"\[(?:GREEN|YELLOW|RED|BLUE|GRAY|NOT_RATED|GREEN_BAR|RED_BAR|YELLOW_BAR|GRAY_BAR|IMAGE|CHART|SEPARATOR|CHECK)\]"
)


@dataclass
class DocConversionResult:
    """Artifacts produced by a .doc -> .md conversion run."""

    markdown: str
    markdown_path: Path
    html_path: Path
    work_dir: Path
    metrics: dict[str, int]
    document_kind: str


def _count_metrics(markdown: str) -> dict[str, int]:
    lines = markdown.splitlines()
    return {
        "chars": len(markdown),
        "lines": len(lines),
        "headings": sum(1 for ln in lines if re.match(r"^#{1,6}\s+", ln)),
        "table_lines": sum(1 for ln in lines if re.match(r"^\|.*\|$", ln.strip())),
        "icon_tokens": len(ICON_PATTERN.findall(markdown)),
    }


def convert_doc_to_markdown(
    doc_path: str | Path,
    output_path: Optional[str | Path] = None,
    *,
    keep_intermediate: bool = False,
    work_dir: Optional[str | Path] = None,
) -> DocConversionResult:
    """
    Convert a Word document to Markdown using the same HTML path as production.

    Pipeline:
      1. LibreOffice: .doc/.docx -> .html (+ asset folder when present)
      2. html_markdown_converter: .html -> .md (tables, headings, rating icons)
    """
    doc_path = Path(doc_path).resolve()
    owns_work_dir = work_dir is None
    if owns_work_dir:
        work_dir = Path(tempfile.mkdtemp(prefix="ewa-doc-md-"))
    else:
        work_dir = Path(work_dir).resolve()
        work_dir.mkdir(parents=True, exist_ok=True)

    document_kind = detect_word_document_kind(doc_path)
    html_path = convert_doc_to_html(doc_path, work_dir / "html")

    if output_path is None:
        output_path = work_dir / f"{doc_path.stem}.md"
    else:
        output_path = Path(output_path).resolve()

    markdown = convert_html_to_markdown(str(html_path), str(output_path))
    metrics = _count_metrics(markdown)

    asset_dirs = discover_companion_dirs(html_path)
    metrics["asset_dirs"] = len(asset_dirs)

    logger.info(
        "Converted %s -> %s (%d chars, %d headings, %d table lines, %d icon tokens)",
        doc_path.name,
        output_path.name,
        metrics["chars"],
        metrics["headings"],
        metrics["table_lines"],
        metrics["icon_tokens"],
    )

    if not keep_intermediate and owns_work_dir:
        # Caller asked for a throwaway work dir; they only need paths in the result.
        pass

    return DocConversionResult(
        markdown=markdown,
        markdown_path=output_path,
        html_path=html_path,
        work_dir=work_dir,
        metrics=metrics,
        document_kind=document_kind,
    )


def compare_markdown(reference_md: str, candidate_md: str) -> dict[str, int | float]:
    """Compare basic structural metrics between two markdown documents."""
    ref = _count_metrics(reference_md)
    cand = _count_metrics(candidate_md)

    def ratio(key: str) -> float:
        base = ref[key] or 1
        return round(cand[key] / base, 3)

    return {
        "reference": ref,
        "candidate": cand,
        "heading_ratio": ratio("headings"),
        "table_line_ratio": ratio("table_lines"),
        "icon_token_ratio": ratio("icon_tokens"),
        "char_ratio": ratio("chars"),
    }


def cleanup_work_dir(work_dir: str | Path) -> None:
    """Remove a temporary conversion directory."""
    shutil.rmtree(work_dir, ignore_errors=True)
