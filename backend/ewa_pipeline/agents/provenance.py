from __future__ import annotations

import re

from ewa_pipeline.report.schemas import DomainAnalysis, Finding, Remediation


DEFAULT_ALLOWED_SOURCES = [
    "SAP Help Portal",
    "SAP Notes / SAP KBAs",
    "SAP Community only as non-authoritative context",
]

_VERSION_SPECIFIC_PATTERNS = (
    r"\bsap note\b",
    r"\bkba\b",
    r"\bcve-\d{4}-\d+\b",
    r"\bkernel\b",
    r"\bsupport package\b",
    r"\bpatch\b",
    r"\bupgrade\b",
    r"\bnetweaver\b",
    r"\bs/4hana\b",
    r"\becc\b",
    r"\babap platform\b",
)

_PARAMETER_PATTERNS = (
    r"\brz10\b",
    r"\brz11\b",
    r"\bparameter\b",
    r"\bprofile\b",
    r"\bset .*=\b",
    r"\bincrease .* to \d",
    r"\bdecrease .* to \d",
    r"\bmemory allocation\b",
    r"\bbuffer size\b",
)

_SECURITY_PATTERNS = (
    r"\bsecurity\b",
    r"\bsap_all\b",
    r"\bsap_new\b",
    r"\brfc\b",
    r"\btls\b",
    r"\bcipher\b",
    r"\bpassword policy\b",
    r"\bauthori[sz]ation\b",
    r"\bvulnerab",
)

_ARCHITECTURE_PATTERNS = (
    r"\bha\b",
    r"\bdr\b",
    r"\bcluster\b",
    r"\bmigration\b",
    r"\bmove workload\b",
    r"\bresiz",
    r"\bscale\b",
    r"\barchitecture\b",
)

_HIGH_IMPACT_PATTERNS = (
    r"\bdowntime\b",
    r"\brestart\b",
    r"\breboot\b",
    r"\bkernel upgrade\b",
    r"\bdatabase parameter\b",
    r"\bdb parameter\b",
    r"\bmass\b.*\bjob\b",
    r"\bdelete\b",
    r"\bremove users?\b",
    r"\block users?\b",
)

_LOW_RISK_INVESTIGATION_PATTERNS = (
    r"\breview\b",
    r"\bcheck\b",
    r"\banaly[sz]e\b",
    r"\binvestigate\b",
    r"\bmonitor\b",
    r"\bvalidate\b",
)


def enrich_domain_analysis_provenance(analysis: DomainAnalysis) -> DomainAnalysis:
    """Return a copy of an analysis with deterministic remediation validation flags."""
    findings = [
        finding.model_copy(update={"remediation": classify_remediation(finding)})
        for finding in analysis.findings
    ]
    return analysis.model_copy(update={"findings": findings})


def classify_remediation(finding: Finding) -> Remediation:
    remediation = finding.remediation
    text = _normalise(
        " ".join(
            [
                finding.title,
                finding.description,
                finding.evidence,
                finding.impact,
                remediation.action,
                " ".join(remediation.sap_transactions),
            ]
        )
    )

    reason = _validation_reason(text, finding)
    if reason is None:
        return remediation.model_copy(
            update={
                "external_validation_required": False,
                "validation_reason": (
                    "Recommendation is report-grounded, covered by local guidance, "
                    "or limited to low-risk investigation."
                ),
                "validation_query": "",
                "allowed_sources": [],
            }
        )

    return remediation.model_copy(
        update={
            "external_validation_required": True,
            "validation_reason": reason,
            "validation_query": _build_validation_query(finding),
            "allowed_sources": DEFAULT_ALLOWED_SOURCES,
        }
    )


def _validation_reason(text: str, finding: Finding) -> str | None:
    if _matches_any(text, _VERSION_SPECIFIC_PATTERNS):
        return "Version-specific SAP guidance or patch information should be validated externally."
    if _matches_any(text, _SECURITY_PATTERNS):
        return "Security-sensitive remediation should be validated against current SAP guidance."
    if _matches_any(text, _PARAMETER_PATTERNS):
        return "Parameter or sizing changes may vary by release, database, OS, and workload."
    if _matches_any(text, _ARCHITECTURE_PATTERNS):
        return "Architecture or operating-model changes require current vendor guidance."
    if _matches_any(text, _HIGH_IMPACT_PATTERNS):
        return "High-impact operational action should be validated before execution."
    if _looks_like_unsupported_best_practice_claim(text):
        return "Best-practice claim lacks an explicit local source and should be validated."
    if finding.severity in {"Critical", "High"} and not _matches_any(
        text, _LOW_RISK_INVESTIGATION_PATTERNS
    ):
        return "High-severity remediation should be externally validated unless it is only triage."
    return None


def _build_validation_query(finding: Finding) -> str:
    transactions = " ".join(finding.remediation.sap_transactions[:3])
    raw = f"SAP {finding.title} {transactions} {finding.remediation.action}"
    return re.sub(r"\s+", " ", raw).strip()[:240]


def _looks_like_unsupported_best_practice_claim(text: str) -> bool:
    return any(
        phrase in text
        for phrase in (
            "sap recommends",
            "recommended by sap",
            "best practice",
            "industry standard",
            "deprecated",
            "unsupported",
        )
    )


def _matches_any(text: str, patterns: tuple[str, ...]) -> bool:
    return any(re.search(pattern, text) for pattern in patterns)


def _normalise(text: str) -> str:
    return re.sub(r"\s+", " ", text.casefold()).strip()
