from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ewa_pipeline.agents.orchestrator import (  # noqa: E402
    _normalise_finding_ids,
    _normalise_section_tasks,
)
from ewa_pipeline.report.schemas import DomainAnalysis, Finding, Remediation  # noqa: E402


class OrchestratorHelperTests(unittest.TestCase):
    def test_section_tasks_drop_unknown_and_duplicate_ids(self) -> None:
        tasks = [
            {"section_id": " [0031] ", "section_title": "Invented", "analysis_focus": "A"},
            {"section_id": "0031", "section_title": "Duplicate", "analysis_focus": "B"},
            {"section_id": "9999", "section_title": "Unknown", "analysis_focus": "C"},
        ]
        sections = [{"id": "0031", "title": "Trusted title"}]

        normalized = _normalise_section_tasks(tasks, sections)

        self.assertEqual(1, len(normalized))
        self.assertEqual("0031", normalized[0]["section_id"])
        self.assertEqual("Trusted title", normalized[0]["section_title"])

    def test_finding_ids_are_unique_across_sections(self) -> None:
        def analysis(section_id: str) -> DomainAnalysis:
            return DomainAnalysis(
                section_title=f"Section {section_id}",
                section_id=section_id,
                findings=[
                    Finding(
                        id="F001",
                        title="Example",
                        severity="Medium",
                        description="Observed issue",
                        evidence="Metric 1",
                        impact="Potential delay",
                        remediation=Remediation(
                            action="Validate the metric",
                            sap_transactions=["ST03N"],
                            effort_estimate="Low",
                            priority="Short-term",
                        ),
                    )
                ],
                overall_health="Warning",
            )

        first = _normalise_finding_ids(analysis("0031"))
        second = _normalise_finding_ids(analysis("0042"))

        self.assertEqual("0031-F001", first.findings[0].id)
        self.assertEqual("0042-F001", second.findings[0].id)
        self.assertNotEqual(first.findings[0].id, second.findings[0].id)


if __name__ == "__main__":
    unittest.main()
