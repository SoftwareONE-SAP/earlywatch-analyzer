"""SAP vs us: compare SAP's own ratings with our findings (no AI)."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from ewa_pipeline.report.reconciliation import clean_title, reconcile
from ewa_pipeline.report.schemas import (
    AnalysisResult,
    DomainAnalysis,
    Finding,
    SapAlert,
    SapCheck,
    SapServiceSummary,
    SectionCoverage,
    SystemProfile,
)

PROFILE = SystemProfile(sid="TP1", db_id="H4P")


def finding(fid: str, severity: str, title: str = "A finding", evidence: str = "") -> Finding:
    return Finding(
        id=fid, title=title, severity=severity, description="d", evidence=evidence, impact="i",
        remediation={"action": "a", "sap_transactions": [], "effort_estimate": "Low", "priority": "Short-term"},
    )


def analysis(section_id: str, *findings: Finding) -> DomainAnalysis:
    return DomainAnalysis(
        section_title=f"S{section_id}", section_id=section_id, findings=list(findings), overall_health="Warning"
    )


def cover(section_id: str, status: str = "analyzed") -> SectionCoverage:
    return SectionCoverage(section_id=section_id, section_title=f"S{section_id}", status=status)


def node(node_id: str, title: str, children: list | None = None) -> dict:
    return {"node_id": node_id, "title": title, "nodes": children or []}


TREE = {"structure": [
    node("0001", "4 Software Configuration for TP1", [
        node("0002", "4.1 Kernel Release *"),
        node("0003", "4.2 Support Packages", [node("0004", "4.2.1 Child Details")]),
    ]),
    node("0005", "5 Database Check for H4P"),
    node("0006", "6 Broken Section"),
    node("0007", "7 Skipped Section"),
]}


def make_result(analyses: list[DomainAnalysis], coverage: list[SectionCoverage]) -> AnalysisResult:
    return AnalysisResult(
        domain_analyses=analyses, cross_references=[], executive_summary="", overall_system_health="Warning",
        top_5_priority_actions=[], token_usage={}, coverage=coverage,
    )


def check(item: str, rating: str, topic: str = "Topic") -> SapCheck:
    return SapCheck(topic=topic, subtopic=item, rating=rating, raw_title=item)


class CleanTitleTests(unittest.TestCase):
    def test_strips_number_marker_sid_and_db_id(self):
        self.assertEqual(clean_title("4.2.1  Kernel   for TP1 *", "TP1", "H4P"), "kernel for")
        self.assertEqual(clean_title("5 Database Check for H4P", "TP1", "H4P"), "database check for")
        self.assertEqual(clean_title("Kernel Release", "", ""), "kernel release")

    def test_sid_only_removed_as_whole_word(self):
        self.assertEqual(clean_title("TP10 and TP1", "TP1"), "tp10 and")

    def test_only_one_trailing_marker(self):
        self.assertEqual(clean_title("Thing * *"), "thing *")


class CheckRowTests(unittest.TestCase):
    def setUp(self):
        self.result = make_result(
            [
                analysis("0002", finding("F-1", "Medium", "Kernel is old")),
                analysis("0004", finding("F-2", "High", "Child problem"), finding("F-3", "Low")),
                analysis("0005"),
            ],
            [cover("0002"), cover("0004"), cover("0005"), cover("0006", "failed"), cover("0007", "skipped")],
        )
        self.summary = SapServiceSummary(checks=[
            check("Kernel Release *", "YELLOW"),      # Agree (Medium = YELLOW)
            check("Support Packages", "GREEN"),       # child High rolls up: We rated higher
            check("Database Check for H4P", "YELLOW"),  # no findings: We rated lower
            check("Broken Section", "RED"),           # failed
            check("Skipped Section", "RED"),          # skipped
            check("Nothing Like This", "RED"),        # no section
            check("Kernel Release", "GRAY"),          # SAP not rated
        ])
        self.rows = {r.sap_item + r.sap_rating: r for r in reconcile(self.result, self.summary, TREE, PROFILE)}

    def verdicts(self):
        return [r.verdict for r in reconcile(self.result, self.summary, TREE, PROFILE)]

    def test_all_verdicts_present(self):
        self.assertEqual(
            self.verdicts(),
            ["Agree", "We rated higher", "We rated lower", "Not covered", "Not covered",
             "No detail section in report", "SAP not rated"],
        )

    def test_child_severity_rolls_up_to_parent(self):
        row = self.rows["Support PackagesGREEN"]
        self.assertEqual(row.our_rating, "RED")
        self.assertEqual(row.our_section_id, "0003")
        self.assertEqual(row.finding_ids, ["F-2", "F-3"])
        self.assertEqual(row.reason, "We raised F-2 (High) 'Child problem' and 1 more")

    def test_reasons(self):
        self.assertEqual(self.rows["Kernel Release *YELLOW"].reason, "We raised F-1 (Medium) 'Kernel is old'")
        self.assertEqual(self.rows["Database Check for H4PYELLOW"].reason, "No finding raised; section analysed")
        self.assertEqual(self.rows["Broken SectionRED"].reason, "Section failed analysis")
        self.assertEqual(self.rows["Skipped SectionRED"].reason, "Section skipped")
        self.assertEqual(self.rows["Nothing Like ThisRED"].reason, "No matching section in report")
        self.assertEqual(self.rows["Database Check for H4PYELLOW"].our_rating, "GREEN")

    def test_old_result_without_coverage_is_not_marked_skipped(self):
        self.result.coverage = []
        rows = reconcile(self.result, self.summary, TREE, PROFILE)
        self.assertEqual(rows[3].verdict, "We rated lower")


class AlertRowTests(unittest.TestCase):
    def setUp(self):
        self.result = make_result(
            [analysis("0002", finding("F-9", "High", "Standard users retain default passwords"))],
            [cover("0002")],
        )

    def run_alert(self, text: str, rating: str = "YELLOW"):
        summary = SapServiceSummary(alerts=[SapAlert(rating=rating, text=text)])
        return reconcile(self.result, summary, TREE, PROFILE)[0]

    def test_match_above_threshold(self):
        row = self.run_alert("Standard users have default password.")
        self.assertEqual(row.source, "Alert")
        self.assertGreaterEqual(row.match_score, 0.3)
        self.assertEqual(row.finding_ids, ["F-9"])
        self.assertEqual(row.our_section_id, "0002")
        self.assertEqual(row.our_rating, "RED")
        self.assertEqual(row.verdict, "We rated higher")

    def test_title_only_score_rescues_long_evidence(self):
        self.result.domain_analyses[0].findings[0].evidence = " ".join(f"word{i}" for i in range(60))
        self.assertEqual(self.run_alert("Standard users default passwords", "RED").verdict, "Agree")

    def test_below_threshold_is_not_covered(self):
        row = self.run_alert("Backup of the database has not run for a week")
        self.assertLess(row.match_score, 0.3)
        self.assertEqual(row.verdict, "Not covered")
        self.assertEqual(row.finding_ids, [])
        self.assertEqual(row.our_rating, "")


class EdgeCaseTests(unittest.TestCase):
    def test_none_or_empty_summary_gives_no_rows(self):
        result = make_result([], [])
        self.assertEqual(reconcile(result, None, TREE, PROFILE), [])
        self.assertEqual(reconcile(result, SapServiceSummary(), TREE, PROFILE), [])

    def test_odd_inputs_do_not_raise(self):
        summary = SapServiceSummary(checks=[check("Kernel", "RED")], alerts=[SapAlert(rating="", text="")])
        rows = reconcile(make_result([], []), summary, None, None)
        self.assertEqual([r.verdict for r in rows], ["Not covered", "No detail section in report"])

    def test_old_payload_defaults_to_empty_reconciliation(self):
        result = AnalysisResult.model_validate({
            "domain_analyses": [], "cross_references": [], "executive_summary": "",
            "overall_system_health": "Unknown", "top_5_priority_actions": [], "token_usage": {},
        })
        self.assertEqual(result.reconciliation, [])


if __name__ == "__main__":
    unittest.main()
