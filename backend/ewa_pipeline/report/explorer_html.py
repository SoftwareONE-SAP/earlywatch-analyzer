"""
Self-contained interactive HTML "explorer" page for one analysis run.

The page is a fixed template (templates/explorer.html) with the run's data filled in as JSON.
The data is built from the in-memory AnalysisResult with the same helpers the Excel workbook
uses, so the page and the workbook always agree.
"""
from __future__ import annotations

import json
from pathlib import Path

from ewa_pipeline.report import reconciliation_display as rd
from ewa_pipeline.report import visual_data as vd
from ewa_pipeline.report.excel_generator import (
    _add_cells, _clean_action, _coverage_lines, _findings_in_order, _refs_in_text,
)
from ewa_pipeline.report.schemas import AnalysisResult

_TEMPLATE = Path(__file__).parent / "templates" / "explorer.html"
_PLACEHOLDER = "/*__DATA__*/null"

_COMPARE_NOTE = "SAP's own ratings next to ours. Results marked as worth a look are where a second opinion helps."
_HEATMAP_NOTE = ("Number = findings of that risk type. Colour = the most serious of them. "
                 "A finding with two risk types counts in both.")

FINDING_COLUMNS = [
    "Ref.", "Severity", "Title", "What it means", "Recommended action",
    "Priority", "Effort", "How sure we are", "Section",
    "Risk area", "What the SAP report says", "Impact", "Why", "How to confirm",
    "SAP transactions", "Check latest SAP guidance first?", "Due date",
    "Reviewer note: why check first", "Reviewer note: search query",
]


def _text(value) -> str:
    """None becomes an empty string; everything else is shown as text."""
    return "" if value is None else str(value)


def _action_parts(text: str) -> tuple[str, str]:
    """Split one action into a short headline (first sentence) and the rest."""
    head, sep, body = text.partition(". ")
    return (head + "." if sep else head), body.strip()


def _finding_dicts(result: AnalysisResult) -> list[dict]:
    rows = []
    for da, f in _findings_in_order(result):
        vals = [
            f.id, f.severity, f.title, f.description, f.remediation.action,
            f.remediation.priority, f.remediation.effort_estimate, f.confidence, da.section_title,
            ", ".join(f.risk_types), f.evidence, f.impact, f.confidence_reason, f.to_confirm,
            ", ".join(f.remediation.sap_transactions),
            "Yes" if f.remediation.external_validation_required else "", f.due_date,
            f.remediation.validation_reason, f.remediation.validation_query,
        ]
        rows.append({col: _text(v) for col, v in zip(FINDING_COLUMNS, vals)})
    return rows


def _compare_block(result: AnalysisResult) -> dict:
    """SAP vs SoftwareONE: result counts and one row per reconciliation row."""
    block: dict = {"note": _COMPARE_NOTE, "summary": [], "rows": []}
    rows, analyses = result.reconciliation, result.domain_analyses
    if not rows:
        return block
    findings_by_id: dict = {}
    for da in analyses:
        for f in da.findings:
            findings_by_id.setdefault(f.id, f)
    block["summary"] = [{"result": name, "alerts": alerts, "checks": checks, "total": alerts + checks}
                        for name, alerts, checks in vd.sap_result_counts(rows, analyses)]
    for row in rows:
        disp = rd.describe(row, findings_by_id)
        finding = findings_by_id.get(row.finding_ids[0]) if row.finding_ids else None
        title = finding.title if finding is not None else ""
        if title and len(row.finding_ids) > 1:
            title += f" (+{len(row.finding_ids) - 1} more)"
        block["rows"].append({
            "SAP list": row.source, "SAP topic": row.sap_topic, "What SAP says": row.sap_item,
            "SAP rating": row.sap_rating.title(), "SoftwareONE rating": row.our_rating.title(),
            "Our finding": title, "Result": disp.result, "How sure we are": disp.how_sure,
            "Explanation": disp.explanation, "Report section": row.our_section_title,
            "Reviewer note: refs": ", ".join(row.finding_ids),
            "Reviewer note: score": _text(row.match_score),
            "Reviewer note: matched by": row.match_method, "Reviewer note: original note": row.reason,
        })
    return block


def _heatmap_block(result: AnalysisResult) -> dict:
    """Sections down, risk types across; a final Total row."""
    rows = vd.heatmap_rows(result)
    risks = vd.heatmap_columns(result)
    block: dict = {"note": _HEATMAP_NOTE, "risks": risks, "rows": []}
    if not rows:
        return block

    def cells_of(cells: dict) -> list[dict]:
        return [{"n": cells[rt][0], "sev": cells[rt][1]} if rt in cells else {"n": 0, "sev": ""}
                for rt in risks]

    totals: dict = {}
    for row in rows:
        block["rows"].append({"section": row.title, "sap": (row.sap_rating or "").title(),
                              "cells": cells_of(row.cells), "total": row.findings})
        _add_cells(totals, row.cells)
    block["rows"].append({"section": "Total", "sap": "", "cells": cells_of(totals),
                          "total": sum(row.findings for row in rows)})
    return block


def build_explorer_data(result: AnalysisResult, source_name: str) -> dict:
    """Everything the explorer page shows, as plain JSON-ready data."""
    sid = result.system_profile.sid if result.system_profile else ""
    findings = _finding_dicts(result)
    known = {f["Ref."] for f in findings}

    actions = []
    for action in result.top_5_priority_actions:
        clean = _clean_action(action)
        head, body = _action_parts(clean)
        actions.append({"head": head, "body": body, "refs": _refs_in_text(clean, result)})

    combos = []
    for xr in result.cross_references:
        why = " ".join(t.strip() for t in (xr.correlation_description, xr.combined_impact) if t.strip())
        if xr.recommended_action.strip():
            why += f"\nWhat to do: {xr.recommended_action.strip()}"
        combos.append({"head": xr.title, "body": why,
                       "refs": list(dict.fromkeys(fid for fid in xr.related_findings if fid in known))})

    return {
        "sid": sid or "",
        "title": f"SAP EarlyWatch Alert \u2014 {sid or 'Deep Analysis Report'}",
        "source": source_name,
        "health": str(result.overall_system_health).upper(),
        "summary": " ".join(text for text, _bold in _coverage_lines(result)),
        "actions": actions,
        "combos": combos,
        "findings": findings,
        "compare": _compare_block(result),
        "heatmap": _heatmap_block(result),
    }


def render_explorer_html(data: dict) -> str:
    """Put the data into the template. "<" is escaped so no text can close the script tag."""
    template = _TEMPLATE.read_text(encoding="utf-8")
    if _PLACEHOLDER not in template:
        raise ValueError(f"Explorer template has no {_PLACEHOLDER} placeholder")
    payload = json.dumps(data, ensure_ascii=False).replace("<", "\\u003c")
    return template.replace(_PLACEHOLDER, payload, 1)


def write_explorer(result: AnalysisResult, path: Path, source_name: str) -> Path:
    """Write the explorer page for one run and return its path."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_explorer_html(build_explorer_data(result, source_name)), encoding="utf-8")
    return path
