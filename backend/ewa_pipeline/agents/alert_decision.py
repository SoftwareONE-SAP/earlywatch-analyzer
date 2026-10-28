"""Ask Decision-1 whether each SAP alert matches each of our findings.

Used by the live pipeline only when config.decision_enabled is on. Never raises:
any problem means "no score", and the caller falls back to word overlap.
"""
from __future__ import annotations

import logging
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Callable

from ewa_pipeline.agents.decision_client import decide
from ewa_pipeline.config import Config
from ewa_pipeline.report.schemas import AnalysisResult, SapServiceSummary

log = logging.getLogger(__name__)

QUESTION = (
    "SAP's EarlyWatch Alert report raised the alert in sap_alert. Our analysis wrote the finding "
    "in finding. Does this finding report the same specific problem that the SAP alert warns about?"
)
CRITERIA = {
    "true": (
        "Yes: the finding is about the same specific problem as the alert (same object and same "
        "kind of issue), even if it uses different words or gives more detail."
    ),
    "false": (
        "No: the finding is about a different problem. Sharing only a general topic (for example "
        "both about SAP HANA, security, or passwords) is not enough."
    ),
}

EVIDENCE_LIMIT = 1500
CALL_TIMEOUT_SECONDS = 15.0


def decision_state(alert: dict, finding: dict, section_title: str) -> dict:
    """The context sent to Decision-1. `alert` has rating+text, `finding` has the Finding fields."""
    return {
        "sap_alert": {"rating": alert["rating"], "text": alert["text"]},
        "finding": {
            "id": finding["id"],
            "section": section_title,
            "severity": finding["severity"],
            "title": finding["title"],
            "evidence": (finding.get("evidence") or "")[:EVIDENCE_LIMIT],
        },
    }


def score_alerts(
    result: AnalysisResult,
    sap_summary: SapServiceSummary | None,
    config: Config,
    *,
    post: Callable[..., Any] | None = None,
    clock: Callable[[], float] = time.monotonic,
) -> dict[int, dict[str, float]]:
    """{alert index (0-based): {finding id: p}} for every alert that was scored in full.

    Returns {} when Decision-1 is off. An alert is left out if any one of its
    calls failed (a partial list could hide the best match). If every call for
    the first alert fails, the service is treated as down and we stop. We also
    stop starting new alerts once decision_budget_seconds has passed.
    """
    try:
        if not config.decision_enabled or sap_summary is None or not sap_summary.alerts:
            return {}
        findings = [(a.section_title, f.model_dump()) for a in result.domain_analyses for f in a.findings]
        if not findings:
            return {}
        deadline = clock() + config.decision_budget_seconds
        scores: dict[int, dict[str, float]] = {}

        def ask(alert: dict, section_title: str, finding: dict) -> dict:
            state = decision_state(alert, finding, section_title)
            return decide(QUESTION, CRITERIA, state, config=config, timeout=CALL_TIMEOUT_SECONDS, post=post)

        with ThreadPoolExecutor(max_workers=config.decision_workers) as pool:
            for index, sap_alert in enumerate(sap_summary.alerts):
                if clock() >= deadline:
                    log.warning("Decision-1 time budget used up; %d alerts left unscored",
                                len(sap_summary.alerts) - index)
                    break
                alert = {"rating": sap_alert.rating, "text": sap_alert.text}
                answers = list(pool.map(lambda item: ask(alert, *item), findings))
                if index == 0 and not any(answers):
                    log.warning("Decision-1 did not answer for the first alert; skipping the rest")
                    break
                if all(answers):
                    scores[index] = {f["id"]: a["true"] for (_, f), a in zip(findings, answers)}
        return scores
    except Exception as exc:  # scoring must never break an analysis
        log.warning("Decision-1 alert scoring failed: %s", exc)
        return {}
