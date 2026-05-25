from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ewa_pipeline.agents.provenance import (  # noqa: E402
    classify_remediation,
    enrich_domain_analysis_provenance,
)
from ewa_pipeline.report.schemas import DomainAnalysis, Finding, Remediation  # noqa: E402


def _finding(*, severity: str = "Medium", action: str, title: str = "Dialog response time") -> Finding:
    return Finding(
        id="F001",
        title=title,
        severity=severity,
        description="Average response time is 2.8s.",
        evidence="Dialog response time: 2.8s",
        impact="Users experience slow dialog steps.",
        remediation=Remediation(
            action=action,
            sap_transactions=["ST03N"],
            effort_estimate="Low",
            priority="Short-term",
        ),
    )


class ProvenanceTests(unittest.TestCase):
    def test_low_risk_investigation_does_not_require_external_validation(self) -> None:
        remediation = classify_remediation(
            _finding(action="Review workload in ST03N and analyze top transactions.")
        )

        self.assertFalse(remediation.external_validation_required)
        self.assertEqual("", remediation.validation_query)
        self.assertEqual([], remediation.allowed_sources)

    def test_kernel_patch_recommendation_requires_external_validation(self) -> None:
        remediation = classify_remediation(
            _finding(
                severity="High",
                title="Outdated SAP kernel",
                action="Plan a kernel patch after checking the relevant SAP Note.",
            )
        )

        self.assertTrue(remediation.external_validation_required)
        self.assertIn("Version-specific", remediation.validation_reason)
        self.assertIn("SAP", remediation.validation_query)
        self.assertIn("SAP Notes / SAP KBAs", remediation.allowed_sources)

    def test_parameter_change_requires_external_validation(self) -> None:
        remediation = classify_remediation(
            _finding(action="Use RZ10 to increase abap/heap_area_total to 8 GB.")
        )

        self.assertTrue(remediation.external_validation_required)
        self.assertIn("Parameter", remediation.validation_reason)

    def test_enrich_domain_analysis_updates_all_findings(self) -> None:
        analysis = DomainAnalysis(
            section_title="Memory",
            section_id="001",
            findings=[
                _finding(action="Review memory history in ST02."),
                _finding(action="Restart the application server after profile parameter changes."),
            ],
            overall_health="Warning",
        )

        enriched = enrich_domain_analysis_provenance(analysis)

        self.assertEqual("Memory", enriched.section_title)
        self.assertFalse(enriched.findings[0].remediation.external_validation_required)
        self.assertTrue(enriched.findings[1].remediation.external_validation_required)


if __name__ == "__main__":
    unittest.main()
