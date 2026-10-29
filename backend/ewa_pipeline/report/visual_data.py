"""Counting helpers shared by every tab of the Excel workbook (no openpyxl here).

One place computes the numbers, so a tile, a chart and a table can never disagree.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

from ewa_pipeline.report import reconciliation_display as rd
from ewa_pipeline.report.schemas import (
    AnalysisResult, DomainAnalysis, Finding, ReconciliationRow,
)

SEVERITIES = ["Critical", "High", "Medium", "Low"]
_SEV_RANK = {sev: i for i, sev in enumerate(SEVERITIES)}
_EFFORT_RANK = {"Low": 0, "Medium": 1, "High": 2}

RATING_ORDER = {"RED": 0, "YELLOW": 1, "GREEN": 2}

# Same order as Finding.risk_types in schemas.py.
RISK_TYPES = ["Security", "Availability", "Performance", "Compliance", "Cost",
              "Data integrity", "Supportability", "Operations"]
NOT_TAGGED = "Not tagged"

OTHER_CHAPTER = "Other"

RESULT_ORDER = [rd.RESULT_AGREE, rd.RESULT_MORE, rd.RESULT_LESS, rd.RESULT_CHECK,
                rd.RESULT_NOT_FOUND, rd.RESULT_NOT_ANALYSED, rd.RESULT_NO_DETAIL,
                rd.RESULT_NO_RATING]

Chapter = tuple[int | None, str]


def severity_totals(result: AnalysisResult) -> dict[str, int]:
    """Findings per severity. Always has all four keys."""
    totals = {sev: 0 for sev in SEVERITIES}
    for da in result.domain_analyses:
        for f in da.findings:
            if f.severity in totals:
                totals[f.severity] += 1
    return totals


def sap_result_counts(rows: list[ReconciliationRow],
                      analyses: list[DomainAnalysis]) -> list[tuple[str, int, int]]:
    """(result label, alerts, checks) in display order, only labels that occur."""
    findings_by_id: dict[str, Finding] = {}
    for da in analyses:
        for f in da.findings:
            findings_by_id.setdefault(f.id, f)
    displays = [rd.describe(row, findings_by_id) for row in rows]
    seen = {d.result for d in displays}
    results = [r for r in RESULT_ORDER if r in seen] + sorted(seen - set(RESULT_ORDER))
    counts = []
    for result_name in results:
        alerts = sum(1 for x, d in zip(rows, displays) if d.result == result_name and x.source == "Alert")
        checks = sum(1 for x, d in zip(rows, displays) if d.result == result_name and x.source == "Check")
        counts.append((result_name, alerts, checks))
    return counts


def sap_rating_by_section(reconciliation: list[ReconciliationRow]) -> dict[str, str]:
    """Worst SAP rating among Check rows that point at each section."""
    sap_rating: dict[str, str] = {}
    for row in reconciliation:
        if row.source != "Check" or row.sap_rating not in RATING_ORDER or not row.our_section_id:
            continue
        best = sap_rating.get(row.our_section_id)
        if best is None or RATING_ORDER[row.sap_rating] < RATING_ORDER[best]:
            sap_rating[row.our_section_id] = row.sap_rating
    return sap_rating


@dataclass
class TopFix:
    finding: Finding
    section_id: str
    section_title: str
    row: int  # row of the finding on its section tab (3 = first finding), for links


def top_fixes(result: AnalysisResult, n: int = 3) -> list[TopFix]:
    """The n findings to fix first: severity, then effort (Low first), then document order."""
    ranked = []
    for sec_idx, da in enumerate(result.domain_analyses):
        for f_idx, f in enumerate(da.findings):
            key = (_SEV_RANK.get(f.severity, len(SEVERITIES)),
                   _EFFORT_RANK.get(f.remediation.effort_estimate, len(_EFFORT_RANK)),
                   sec_idx, f_idx)
            ranked.append((key, TopFix(f, da.section_id, da.section_title, 3 + f_idx)))
    ranked.sort(key=lambda t: t[0])
    return [fix for _key, fix in ranked[:n]]


def chapter_of(result: AnalysisResult) -> dict[str, Chapter]:
    """section id -> (chapter number, chapter title), guessed from numbered section titles."""
    chapter_titles: dict[int, str] = {}
    mapping: dict[str, Chapter] = {}
    current: Chapter = (None, OTHER_CHAPTER)

    for cov in result.coverage:
        title = cov.section_title.strip()
        start = re.match(r"^(\d+)\s", title)
        member = re.match(r"^(\d+)\.", title)
        if start:
            no = int(start.group(1))
            chapter_titles.setdefault(no, title)
            current = (no, chapter_titles[no])
            mapping.setdefault(cov.section_id, current)
        elif member:
            no = int(member.group(1))
            mapping.setdefault(cov.section_id, (no, chapter_titles.get(no, f"Chapter {no}")))
        else:
            mapping.setdefault(cov.section_id, current)

    # Sections missing from coverage (older payloads): use the number in their own title.
    for da in result.domain_analyses:
        if da.section_id in mapping:
            continue
        lead = re.match(r"^\s*(\d+)", da.section_title)
        if lead:
            no = int(lead.group(1))
            mapping[da.section_id] = (no, chapter_titles.get(no, f"Chapter {no}"))
        else:
            mapping[da.section_id] = (None, OTHER_CHAPTER)
    return mapping


@dataclass
class HeatRow:
    section_id: str
    title: str
    sap_rating: str | None
    # Only risk types that occur: {type: (finding count, worst severity)}.
    cells: dict[str, tuple[int, str]] = field(default_factory=dict)
    findings: int = 0  # distinct findings (a finding with 2 risk types counts once)
    chapter: Chapter = (None, OTHER_CHAPTER)


def heatmap_columns(result: AnalysisResult) -> list[str]:
    """The 8 risk types, plus "Not tagged" only when some finding has no risk type."""
    untagged = any(not f.risk_types for da in result.domain_analyses for f in da.findings)
    return RISK_TYPES + ([NOT_TAGGED] if untagged else [])


def heatmap_rows(result: AnalysisResult) -> list[HeatRow]:
    """Sections with findings, plus sections SAP rated RED or YELLOW, in document order."""
    sap = sap_rating_by_section(result.reconciliation)
    chapters = chapter_of(result)
    flagged = {sid for sid, rating in sap.items() if rating in ("RED", "YELLOW")}

    coverage_index = {cov.section_id: i for i, cov in enumerate(result.coverage)}
    titles = {cov.section_id: cov.section_title.strip() for cov in result.coverage}
    analyses = {}
    for order, da in enumerate(result.domain_analyses):
        analyses.setdefault(da.section_id, (order, da))

    wanted = {sid for sid, (_o, da) in analyses.items() if da.findings} | flagged
    far = len(result.coverage)
    ordered = sorted(wanted, key=lambda sid: (coverage_index.get(sid, far),
                                              analyses[sid][0] if sid in analyses else 0))

    rows = []
    for sid in ordered:
        da = analyses[sid][1] if sid in analyses else None
        row = HeatRow(
            section_id=sid,
            title=(da.section_title if da else titles.get(sid)) or sid,
            sap_rating=sap.get(sid),
            chapter=chapters.get(sid, (None, OTHER_CHAPTER)),
        )
        for f in (da.findings if da else []):
            row.findings += 1
            for rt in (f.risk_types or [NOT_TAGGED]):
                count, worst = row.cells.get(rt, (0, f.severity))
                if _SEV_RANK.get(f.severity, 9) < _SEV_RANK.get(worst, 9):
                    worst = f.severity
                row.cells[rt] = (count + 1, worst)
        rows.append(row)
    return rows
