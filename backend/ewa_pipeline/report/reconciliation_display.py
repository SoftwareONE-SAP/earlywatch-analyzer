"""Plain-English wording for "SAP vs SoftwareONE" rows.

Turns the stored ReconciliationRow fields into Result / How sure / Explanation
for people who do not know how the matching works. Presentation only: it reads
rows, never changes them. Old saved rows lack `match_method`, so the reason
text is parsed when needed.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

from ewa_pipeline.report.schemas import ReconciliationRow

RESULT_AGREE = "Agree"
RESULT_MORE = "We rate it more serious"
RESULT_LESS = "We rate it less serious"
RESULT_CHECK = "Please check"
RESULT_NOT_FOUND = "Not found in our analysis"
RESULT_NOT_ANALYSED = "Section not analysed"
RESULT_NO_DETAIL = "No detail to compare"
RESULT_NO_RATING = "SAP gave no rating"

_RESULT_BY_VERDICT = {
    "Agree": RESULT_AGREE,
    "We rated higher": RESULT_MORE,
    "We rated lower": RESULT_LESS,
    "SAP not rated": RESULT_NO_RATING,
    "No detail section in report": RESULT_NO_DETAIL,
}

_D1_RE = re.compile(r"Decision-1 match \(p=([\d.]+)\)")
_CANDIDATE_RE = re.compile(r"please check: (\S+) '(.*?)' \(p=([\d.]+)\)")
_RAISED_RE = re.compile(r"We raised (\S+) \((\w+)\) '(.*?)'")


@dataclass(frozen=True)
class RowDisplay:
    result: str
    how_sure: str  # "High", "Medium", "Low" or "" when nothing was matched
    explanation: str
    needs_attention: bool = False  # True for rows a reader should look at


def _colour(rating: str) -> str:
    return (rating or "").title()


def _finding_label(row: ReconciliationRow, findings_by_id: dict) -> str:
    """Title and severity of the first matched finding, from the finding or the old reason text."""
    finding = findings_by_id.get(row.finding_ids[0]) if row.finding_ids else None
    if finding is not None:
        return f"'{finding.title}' ({finding.severity})"
    m = _RAISED_RE.search(row.reason or "")
    if m:
        return f"'{m.group(3)}' ({m.group(2)})"
    return f"'{row.our_section_title}'" if row.our_section_title else "a finding"


def _candidate(row: ReconciliationRow, findings_by_id: dict) -> str:
    """Name the 'please check' finding from the reason text, or empty when there is none."""
    m = _CANDIDATE_RE.search(row.reason or "")
    if not m:
        return ""
    finding = findings_by_id.get(m.group(1))
    title = finding.title if finding is not None else m.group(2)
    return f"{m.group(1)} '{title}'"


def _alert_how_sure(row: ReconciliationRow) -> str:
    """Confidence for an alert that was matched to a finding."""
    if row.match_method in ("Report heading", "Same SQL statement"):
        return "Medium"
    reason = row.reason or ""
    m = _D1_RE.search(reason)
    if row.match_method == "Decision-1" or m:
        if row.match_method == "Decision-1" and row.match_score is not None:
            p = row.match_score
        else:
            p = float(m.group(1)) if m else 1.0
        close = "also close, please check" in reason
        return "Medium" if close or p < 0.9 else "High"
    if "Decision-1 did not confirm" in reason or "Decision-1 possible match" in reason:
        return "Low"
    return "Medium"


def describe(row: ReconciliationRow, findings_by_id: dict) -> RowDisplay:
    """Result, how sure and a one-sentence explanation for one comparison row."""
    verdict = row.verdict or ""
    reason = row.reason or ""
    sap = _colour(row.sap_rating)
    ours = _colour(row.our_rating)

    if row.source == "Check":
        return _describe_check(row, findings_by_id, verdict, sap, ours)

    if verdict == "Not covered":
        candidate = _candidate(row, findings_by_id)
        if candidate:
            return RowDisplay(
                RESULT_CHECK, "Low",
                f"We could not confirm a match, but {candidate} may be the same issue. "
                "Please compare the two by hand.",
                needs_attention=True,
            )
        return RowDisplay(RESULT_NOT_FOUND, "", "No finding in our analysis matches this SAP alert.",
                          needs_attention=True)

    result = _RESULT_BY_VERDICT.get(verdict, verdict or RESULT_NO_DETAIL)
    sure = _alert_how_sure(row)
    text = _matched_sentence(verdict, sap, ours, _finding_label(row, findings_by_id))
    if row.match_method == "Report heading":
        text += " We chose it because it sits under the report heading that uses SAP's own wording."
    elif row.match_method == "Same SQL statement":
        text += " We chose it because it is about the same SQL statement that SAP's report lists for this alert."
    extra = _candidate(row, findings_by_id)
    if extra and ("also close" in reason or "Decision-1 possible match" in reason):
        text += f" Another finding may also relate: {extra}."
    elif sure == "Low":
        text += " Our match is only a rough word match, so please check it."
    return RowDisplay(result, sure, text, needs_attention=verdict in ("We rated higher", "We rated lower"))


def _matched_sentence(verdict: str, sap: str, ours: str, label: str) -> str:
    if verdict == "Agree":
        return f"SAP and SoftwareONE both rate this {sap}. We matched it to {label}."
    if verdict == "We rated higher":
        return f"SAP rates this {sap}. We found {label}, so we rate it {ours}."
    if verdict == "We rated lower":
        return f"SAP rates this {sap}. We found {label}, which we rate {ours}."
    return f"SAP gave no colour rating. We matched it to {label}."


def _describe_check(row, findings_by_id, verdict, sap, ours) -> RowDisplay:
    if verdict == "No detail section in report":
        return RowDisplay(RESULT_NO_DETAIL, "",
                          "The report has no detail section for this SAP check, so there is nothing to compare.")
    if verdict == "Not covered":
        why = "could not be analysed" if "failed" in (row.reason or "").lower() else "was not analysed"
        return RowDisplay(RESULT_NOT_ANALYSED, "",
                          f"The matching section {why}, so we cannot compare it with SAP.",
                          needs_attention=True)
    result = _RESULT_BY_VERDICT.get(verdict, verdict or RESULT_NO_DETAIL)
    sure = "High" if row.our_section_id else ""
    if row.finding_ids:
        text = _matched_sentence(verdict, sap, ours, _finding_label(row, findings_by_id))
        if len(row.finding_ids) > 1:
            n = len(row.finding_ids) - 1
            text += f" There {'is' if n == 1 else 'are'} {n} more finding{'' if n == 1 else 's'} in this section."
    elif verdict == "SAP not rated":
        text = "SAP gave no colour rating. We analysed the matching section and raised no finding."
    elif verdict == "Agree":
        text = f"SAP and SoftwareONE both rate this {sap}. We analysed the matching section and raised no finding."
    else:
        text = f"SAP rates this {sap}. We analysed the matching section and raised no finding."
    return RowDisplay(result, sure, text, needs_attention=verdict in ("We rated higher", "We rated lower"))
