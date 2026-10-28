"""Plain-English wording for SAP vs SoftwareONE rows."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from ewa_pipeline.report.reconciliation_display import describe
from ewa_pipeline.report.schemas import Finding, ReconciliationRow


def finding(fid, severity, title):
    return Finding(
        id=fid, title=title, severity=severity, description="d", evidence="", impact="i",
        remediation={"action": "a", "sap_transactions": [], "effort_estimate": "Low", "priority": "Short-term"},
    )


FINDINGS = {
    "F-001": finding("F-001", "High", "Missing backup"),
    "F-002": finding("F-002", "Low", "Old kernel"),
}


def alert(**kw):
    base = dict(source="Alert", sap_item="Backup missing", sap_rating="RED")
    base.update(kw)
    return ReconciliationRow(**base)


def check(**kw):
    base = dict(source="Check", sap_topic="Backup", sap_item="Backup", sap_rating="GREEN")
    base.update(kw)
    return ReconciliationRow(**base)


class DescribeTests(unittest.TestCase):
    def test_decision1_agree_high(self):
        d = describe(alert(verdict="Agree", our_rating="RED", finding_ids=["F-001"], match_method="Decision-1",
                           match_score=0.97,
                           reason="Decision-1 match (p=0.97): We raised F-001 (High) 'Missing backup'"), FINDINGS)
        self.assertEqual((d.result, d.how_sure), ("Agree", "High"))
        self.assertIn("Missing backup", d.explanation)
        self.assertFalse(d.needs_attention)

    def test_decision1_with_close_second_is_medium(self):
        reason = ("Decision-1 match (p=0.95): We raised F-001 (High) 'Missing backup'; "
                  "also close, please check: F-002 'Old kernel' (p=0.93)")
        d = describe(alert(verdict="Agree", our_rating="RED", finding_ids=["F-001"], match_method="Decision-1",
                           match_score=0.95, reason=reason), FINDINGS)
        self.assertEqual(d.how_sure, "Medium")
        self.assertIn("F-002 'Old kernel'", d.explanation)

    def test_word_overlap_only_is_medium(self):
        d = describe(alert(verdict="We rated lower", sap_rating="RED", our_rating="YELLOW", finding_ids=["F-001"],
                           match_method="Word overlap", match_score=0.6,
                           reason="We raised F-001 (High) 'Missing backup'"), FINDINGS)
        self.assertEqual((d.result, d.how_sure), ("We rate it less serious", "Medium"))
        self.assertTrue(d.needs_attention)

    def test_word_overlap_not_confirmed_is_low(self):
        d = describe(alert(verdict="We rated higher", sap_rating="YELLOW", our_rating="RED", finding_ids=["F-001"],
                           match_method="Word overlap",
                           reason="We raised F-001 (High) 'Missing backup'; Decision-1 did not confirm this match"),
                     FINDINGS)
        self.assertEqual((d.result, d.how_sure), ("We rate it more serious", "Low"))
        self.assertIn("rough word match", d.explanation)

    def test_possible_match_is_please_check(self):
        d = describe(alert(verdict="Not covered",
                           reason="No confirmed match. Possible match, please check: F-002 'Old kernel' (p=0.70)"),
                     FINDINGS)
        self.assertEqual((d.result, d.how_sure), ("Please check", "Low"))
        self.assertIn("F-002 'Old kernel'", d.explanation)
        self.assertTrue(d.needs_attention)

    def test_not_found(self):
        d = describe(alert(verdict="Not covered", reason="No finding matches this alert"), FINDINGS)
        self.assertEqual((d.result, d.how_sure), ("Not found in our analysis", ""))

    def test_alert_sap_not_rated(self):
        d = describe(alert(verdict="SAP not rated", sap_rating="GRAY", our_rating="RED", finding_ids=["F-001"],
                           match_method="Word overlap", reason="We raised F-001 (High) 'Missing backup'"), FINDINGS)
        self.assertEqual(d.result, "SAP gave no rating")

    def test_legacy_decision1_row(self):
        d = describe(alert(verdict="Agree", our_rating="RED", finding_ids=["F-001"],
                           reason="Decision-1 match (p=0.92): We raised F-001 (High) 'Missing backup'"), FINDINGS)
        self.assertEqual((d.result, d.how_sure), ("Agree", "High"))

    def test_legacy_word_row_without_known_finding(self):
        d = describe(alert(verdict="Agree", our_rating="RED", finding_ids=["F-999"],
                           reason="We raised F-999 (High) 'Gone title'"), {})
        self.assertEqual(d.how_sure, "Medium")
        self.assertIn("Gone title", d.explanation)

    def test_legacy_please_check_without_findings_map(self):
        d = describe(alert(verdict="Not covered",
                           reason="No confirmed match. Possible match, please check: F-050 'Some title' (p=0.60)"),
                     {})
        self.assertEqual(d.result, "Please check")
        self.assertIn("F-050 'Some title'", d.explanation)

    def test_check_agree_with_finding(self):
        d = describe(check(verdict="Agree", sap_rating="RED", our_rating="RED", our_section_id="0002",
                           finding_ids=["F-001"], reason="We raised F-001 (High) 'Missing backup'"), FINDINGS)
        self.assertEqual((d.result, d.how_sure), ("Agree", "High"))

    def test_check_higher_with_more_findings(self):
        d = describe(check(verdict="We rated higher", sap_rating="GREEN", our_rating="RED", our_section_id="0002",
                           finding_ids=["F-001", "F-002"]), FINDINGS)
        self.assertEqual(d.result, "We rate it more serious")
        self.assertIn("1 more finding ", d.explanation + " ")

    def test_check_green_no_findings(self):
        d = describe(check(verdict="Agree", our_rating="GREEN", our_section_id="0002",
                           reason="No finding raised; section analysed"), FINDINGS)
        self.assertIn("raised no finding", d.explanation)

    def test_check_not_analysed(self):
        for reason, word in (("Section skipped", "was not analysed"),
                             ("Section failed analysis", "could not be analysed")):
            d = describe(check(verdict="Not covered", our_section_id="0002", reason=reason), FINDINGS)
            self.assertEqual((d.result, d.how_sure), ("Section not analysed", ""))
            self.assertIn(word, d.explanation)

    def test_check_no_detail_section(self):
        d = describe(check(verdict="No detail section in report", reason="No matching section in report"), FINDINGS)
        self.assertEqual((d.result, d.how_sure), ("No detail to compare", ""))

    def test_check_sap_not_rated(self):
        d = describe(check(verdict="SAP not rated", sap_rating="GRAY", our_rating="GREEN", our_section_id="0002"),
                     FINDINGS)
        self.assertEqual((d.result, d.how_sure), ("SAP gave no rating", "High"))

    def test_no_internal_words_leak(self):
        rows = [
            alert(verdict="Agree", our_rating="RED", finding_ids=["F-001"], match_method="Decision-1",
                  match_score=0.97, reason="Decision-1 match (p=0.97): We raised F-001 (High) 'Missing backup'"),
            alert(verdict="Not covered",
                  reason="No confirmed match. Possible match, please check: F-002 'Old kernel' (p=0.70)"),
        ]
        for r in rows:
            d = describe(r, FINDINGS)
            for text in (d.result, d.explanation):
                self.assertNotIn("Decision", text)
                self.assertNotIn("p=", text)
                self.assertNotIn("overlap", text)


if __name__ == "__main__":
    unittest.main()
