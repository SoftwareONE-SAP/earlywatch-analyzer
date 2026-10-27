"""Old saved analyses must keep loading after optional Finding fields were added."""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from pydantic import ValidationError
from ewa_pipeline.report.schemas import AnalysisResult, Finding

NEW_FIELDS = ("confidence", "confidence_reason", "to_confirm", "risk_types", "subject", "due_date")


def old_finding() -> dict:
    """A finding shaped like a payload saved before the new fields existed."""
    return {
        "id": "F-001",
        "title": "Kernel release out of maintenance",
        "severity": "High",
        "description": "The kernel is old.",
        "evidence": "Kernel 753 [RED]",
        "impact": "No security patches.",
        "remediation": {
            "action": "Upgrade the kernel.",
            "sap_transactions": ["SPAM"],
            "effort_estimate": "Medium",
            "priority": "Short-term",
        },
    }


def old_payload() -> dict:
    return {
        "domain_analyses": [{
            "section_title": "Software Configuration",
            "section_id": "0001",
            "findings": [old_finding()],
            "overall_health": "Warning",
        }],
        "cross_references": [],
        "executive_summary": "Summary.",
        "overall_system_health": "Warning",
        "top_5_priority_actions": ["Upgrade the kernel."],
        "token_usage": {},
    }


def new_finding() -> dict:
    finding = old_finding()
    finding.update({
        "confidence": "Medium",
        "confidence_reason": "Inferred from the kernel version and the skill threshold.",
        "to_confirm": "Run SM51 and check the kernel release.",
        "risk_types": ["Security", "Supportability"],
        "subject": "kernel 753",
        "due_date": "2027-12-31",
    })
    return finding


class SchemaCompatTests(unittest.TestCase):
    def assert_defaults(self, finding: Finding) -> None:
        self.assertIsNone(finding.confidence)
        self.assertEqual(finding.confidence_reason, "")
        self.assertEqual(finding.to_confirm, "")
        self.assertEqual(finding.risk_types, [])
        self.assertEqual(finding.subject, "")
        self.assertEqual(finding.due_date, "")

    def test_old_payload_loads_from_dict_with_defaults(self):
        result = AnalysisResult.model_validate(old_payload())
        finding = result.domain_analyses[0].findings[0]
        self.assertEqual(finding.id, "F-001")
        self.assert_defaults(finding)

    def test_old_payload_loads_from_json_string_with_defaults(self):
        result = AnalysisResult.model_validate_json(json.dumps(old_payload()))
        self.assert_defaults(result.domain_analyses[0].findings[0])

    def test_finding_with_all_new_fields_round_trips(self):
        payload = old_payload()
        payload["domain_analyses"][0]["findings"] = [new_finding()]
        result = AnalysisResult.model_validate(payload)
        reloaded = AnalysisResult.model_validate_json(result.model_dump_json())
        self.assertEqual(reloaded, result)
        finding = reloaded.domain_analyses[0].findings[0]
        self.assertEqual(finding.confidence, "Medium")
        self.assertEqual(finding.risk_types, ["Security", "Supportability"])
        self.assertEqual(finding.subject, "kernel 753")
        self.assertEqual(finding.due_date, "2027-12-31")

    def test_invalid_risk_type_is_rejected(self):
        data = new_finding()
        data["risk_types"] = ["Fun"]
        with self.assertRaises(ValidationError):
            Finding.model_validate(data)

    def test_invalid_confidence_is_rejected(self):
        data = new_finding()
        data["confidence"] = "Certain"
        with self.assertRaises(ValidationError):
            Finding.model_validate(data)


if __name__ == "__main__":
    unittest.main()
