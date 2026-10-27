"""Compare our findings with SAP's own ratings from the Service Summary.

Plain Python, no AI. SAP colours: RED > YELLOW > GREEN. Our severities map to
colours like this: Critical/High = RED, Medium = YELLOW, Low or none = GREEN.
"""
from __future__ import annotations

import logging
import re

from ewa_pipeline.indexer.tree_navigator import TreeNode, flatten_tree
from ewa_pipeline.report.schemas import (
    AnalysisResult,
    Finding,
    ReconciliationRow,
    SapServiceSummary,
    SystemProfile,
)

logger = logging.getLogger(__name__)

ALERT_MATCH_THRESHOLD = 0.3

_SEVERITY_ORDER = {"Low": 0, "Medium": 1, "High": 2, "Critical": 3}
_COLOUR_BY_SEVERITY = {"Critical": "RED", "High": "RED", "Medium": "YELLOW", "Low": "GREEN"}
_COLOUR_ORDER = {"GREEN": 0, "YELLOW": 1, "RED": 2}

# Very common words are dropped so they do not make unrelated texts look alike.
_STOP_WORDS = frozenset(
    "a an and are as at be by for from has have in is it its of on or that the this to was were with".split()
)
_WORD_RE = re.compile(r"[a-z0-9]+")
_LEADING_NUMBER_RE = re.compile(r"^\s*\d+(?:\.\d+)*\.?\s+")


def clean_title(title: str, sid: str = "", db_id: str = "") -> str:
    """Normalise a heading or SAP check name so the two can be compared."""
    text = _LEADING_NUMBER_RE.sub("", title or "")
    if text.endswith(" *"):
        text = text[:-2]
    for ident in (sid, db_id):
        if ident:
            text = re.sub(rf"\b{re.escape(ident)}\b", " ", text, flags=re.IGNORECASE)
    return re.sub(r"\s+", " ", text).strip().lower()


def _words(text: str) -> set[str]:
    return {w for w in _WORD_RE.findall((text or "").lower()) if w not in _STOP_WORDS}


def _colour(severity: str) -> str:
    return _COLOUR_BY_SEVERITY.get(severity, "GREEN")


def _worst(findings: list[Finding]) -> Finding | None:
    return max(findings, key=lambda f: _SEVERITY_ORDER.get(f.severity, 0), default=None)


def _verdict(sap_rating: str, our_rating: str) -> str:
    # GRAY, NOT_RATED, BLUE or empty: SAP gave no colour, so there is nothing to compare.
    if sap_rating not in _COLOUR_ORDER:
        return "SAP not rated"
    sap, ours = _COLOUR_ORDER[sap_rating], _COLOUR_ORDER[our_rating]
    if ours == sap:
        return "Agree"
    return "We rated higher" if ours > sap else "We rated lower"


def _raised_reason(findings: list[Finding]) -> str:
    worst = _worst(findings)
    reason = f"We raised {worst.id} ({worst.severity}) '{worst.title}'"
    if len(findings) > 1:
        reason += f" and {len(findings) - 1} more"
    return reason


def _descendants(node: TreeNode) -> list[TreeNode]:
    found = [node]
    for child in node.children:
        found.extend(_descendants(child))
    return found


def _jaccard(a: set[str], b: set[str]) -> float:
    union = a | b
    return len(a & b) / len(union) if union else 0.0


def _alert_score(alert_words: set[str], finding: Finding) -> float:
    """Jaccard (shared distinct words / all distinct words), best of two views.

    Long evidence text can water down a good match, so the title alone is
    scored too and the higher score wins.
    """
    title_words = _words(finding.title)
    return max(
        _jaccard(alert_words, title_words),
        _jaccard(alert_words, title_words | _words(finding.evidence)),
    )


def reconcile(
    result: AnalysisResult,
    sap_summary: SapServiceSummary | None,
    tree: dict | None,
    profile: SystemProfile | None,
) -> list[ReconciliationRow]:
    """One row per SAP alert and per SAP check. Never raises on odd input."""
    try:
        if sap_summary is None or not (sap_summary.alerts or sap_summary.checks):
            return []
        sid = profile.sid if profile else ""
        db_id = profile.db_id if profile else ""

        findings_by_section: dict[str, list[Finding]] = {}
        section_of: dict[str, str] = {}
        for analysis in result.domain_analyses:
            findings_by_section.setdefault(analysis.section_id, []).extend(analysis.findings)
            for finding in analysis.findings:
                section_of[finding.id] = analysis.section_id
        coverage = {c.section_id: c for c in result.coverage}

        nodes: list[TreeNode] = []
        for top in flatten_tree(tree or {}):
            nodes.extend(_descendants(top))
        by_title: dict[str, TreeNode] = {}
        for node in nodes:
            by_title.setdefault(clean_title(node.title, sid, db_id), node)
        title_of = {n.id: n.title for n in nodes}

        all_findings = [f for a in result.domain_analyses for f in a.findings]
        rows = [_alert_row(a, all_findings, section_of, title_of) for a in sap_summary.alerts]
        rows += [
            _check_row(c, by_title, findings_by_section, coverage, sid, db_id) for c in sap_summary.checks
        ]
        return rows
    except Exception as exc:  # reconciliation must never break an analysis
        logger.warning("Reconciliation failed: %s", exc)
        return []


def _check_row(check, by_title, findings_by_section, coverage, sid, db_id) -> ReconciliationRow:
    item = check.subtopic or check.topic
    row = ReconciliationRow(source="Check", sap_topic=check.topic, sap_item=item, sap_rating=check.rating)
    node = by_title.get(clean_title(item, sid, db_id))
    if node is None:
        row.verdict = "No detail section in report"
        row.reason = "No matching section in report"
        return row
    row.our_section_id, row.our_section_title = node.id, node.title

    family = _descendants(node)
    findings = [f for n in family for f in findings_by_section.get(n.id, [])]
    row.finding_ids = [f.id for f in findings]
    statuses = [coverage[n.id] for n in family if n.id in coverage]
    # No coverage data at all (old payload) means we cannot say it was skipped.
    if coverage and not any(s.status == "analyzed" for s in statuses):
        failed = any(s.status == "failed" for s in statuses)
        row.verdict = "Not covered"
        row.reason = "Section failed analysis" if failed else "Section skipped"
        return row

    worst = _worst(findings)
    row.our_rating = _colour(worst.severity) if worst else "GREEN"
    row.reason = _raised_reason(findings) if findings else "No finding raised; section analysed"
    row.verdict = _verdict(check.rating, row.our_rating)
    return row


def _alert_row(alert, findings, section_of, title_of) -> ReconciliationRow:
    row = ReconciliationRow(source="Alert", sap_item=alert.text, sap_rating=alert.rating)
    alert_words = _words(alert.text)
    best, best_score = None, 0.0
    for finding in findings:
        score = _alert_score(alert_words, finding)
        if score > best_score:
            best, best_score = finding, score
    row.match_score = round(best_score, 3)
    if best is None or best_score < ALERT_MATCH_THRESHOLD:
        row.verdict = "Not covered"
        row.reason = "No finding matches this alert"
        return row
    section_id = section_of.get(best.id, "")
    row.our_section_id = section_id
    row.our_section_title = title_of.get(section_id, "")
    row.finding_ids = [best.id]
    row.our_rating = _colour(best.severity)
    row.reason = _raised_reason([best])
    row.verdict = _verdict(alert.rating, row.our_rating)
    return row
