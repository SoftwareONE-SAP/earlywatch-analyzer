"""The shared counting helpers behind the workbook visuals."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ewa_pipeline.report import visual_data as vd
from ewa_pipeline.report.schemas import (
    AnalysisResult, DomainAnalysis, Finding, ReconciliationRow, Remediation, SectionCoverage,
)
from ewa_pipeline.tracking.token_tracker import TokenUsage


def _finding(fid: str, severity: str = "Medium", effort: str = "Medium",
             risk_types: list | None = None) -> Finding:
    return Finding(
        id=fid, title=f"Title {fid}", severity=severity, description="d", evidence="e",
        impact="i",
        remediation=Remediation(action="a", sap_transactions=[], effort_estimate=effort,
                                priority="Short-term"),
        risk_types=risk_types or [],
    )


def _da(sid: str, title: str, findings: list[Finding]) -> DomainAnalysis:
    return DomainAnalysis(section_title=title, section_id=sid, findings=findings,
                          overall_health="Warning" if findings else "Healthy")


def _cov(sid: str, title: str) -> SectionCoverage:
    return SectionCoverage(section_id=sid, section_title=title, status="analyzed")


def _result(analyses, coverage=None, reconciliation=None) -> AnalysisResult:
    return AnalysisResult(
        domain_analyses=analyses, cross_references=[], executive_summary="",
        overall_system_health="Warning", top_5_priority_actions=[],
        token_usage=TokenUsage(), coverage=coverage or [], reconciliation=reconciliation or [],
    )


def _check(sid: str, rating: str) -> ReconciliationRow:
    return ReconciliationRow(source="Check", sap_rating=rating, our_section_id=sid)


class SeverityTotalsTests(unittest.TestCase):
    def test_always_four_keys(self):
        self.assertEqual(vd.severity_totals(_result([])),
                         {"Critical": 0, "High": 0, "Medium": 0, "Low": 0})

    def test_counts(self):
        res = _result([_da("1", "A", [_finding("F1", "High"), _finding("F2", "High")]),
                       _da("2", "B", [_finding("F3", "Low")])])
        self.assertEqual(vd.severity_totals(res),
                         {"Critical": 0, "High": 2, "Medium": 0, "Low": 1})


class SapPartsTests(unittest.TestCase):
    def test_worst_rating_wins_and_empty_ids_skipped(self):
        rows = [_check("1", "GREEN"), _check("1", "RED"), _check("1", "YELLOW"),
                _check("2", "YELLOW"), _check("", "RED"),
                ReconciliationRow(source="Alert", sap_rating="RED", our_section_id="3")]
        self.assertEqual(vd.sap_rating_by_section(rows), {"1": "RED", "2": "YELLOW"})

    def test_no_reconciliation_gives_empty_parts(self):
        self.assertEqual(vd.sap_rating_by_section([]), {})
        self.assertEqual(vd.sap_result_counts([], []), [])


class TopFixesTests(unittest.TestCase):
    def test_severity_then_effort_then_order(self):
        res = _result([
            _da("1", "A", [_finding("F1", "High", "Low"), _finding("F2", "Critical", "High")]),
            _da("2", "B", [_finding("F3", "Critical", "Low"), _finding("F4", "Critical", "Low")]),
        ])
        got = [t.finding.id for t in vd.top_fixes(res, n=4)]
        self.assertEqual(got, ["F3", "F4", "F2", "F1"])

    def test_ties_keep_section_then_finding_order(self):
        res = _result([_da("1", "A", [_finding("F1"), _finding("F2")]),
                       _da("2", "B", [_finding("F3")])])
        got = vd.top_fixes(res, n=3)
        self.assertEqual([t.finding.id for t in got], ["F1", "F2", "F3"])
        self.assertEqual([t.row for t in got], [3, 4, 3])
        self.assertEqual(got[2].section_id, "2")

    def test_limit(self):
        res = _result([_da("1", "A", [_finding(f"F{i}") for i in range(5)])])
        self.assertEqual(len(vd.top_fixes(res)), 3)


class ChapterTests(unittest.TestCase):
    def test_unnumbered_title_after_chapter_takes_that_chapter(self):
        res = _result(
            [_da("a", "x", []), _da("b", "x", []), _da("c", "x", []), _da("d", "x", [])],
            coverage=[_cov("a", "13 SAP HANA Database"), _cov("b", "13.1 Alerts"),
                      _cov("c", "Trend Analysis"), _cov("d", "14 Other Stuff")],
        )
        got = vd.chapter_of(res)
        self.assertEqual(got["a"], (13, "13 SAP HANA Database"))
        self.assertEqual(got["b"], (13, "13 SAP HANA Database"))
        self.assertEqual(got["c"], (13, "13 SAP HANA Database"))
        self.assertEqual(got["d"], (14, "14 Other Stuff"))

    def test_unnumbered_before_any_chapter_is_other(self):
        res = _result([], coverage=[_cov("a", "Intro"), _cov("b", "1 First")])
        got = vd.chapter_of(res)
        self.assertEqual(got["a"], (None, "Other"))
        self.assertEqual(got["b"], (1, "1 First"))

    def test_member_without_known_chapter_title(self):
        res = _result([], coverage=[_cov("a", "5.2 Orphan")])
        self.assertEqual(vd.chapter_of(res)["a"], (5, "Chapter 5"))

    def test_section_not_in_coverage_uses_own_title(self):
        res = _result([_da("a", "7.1 Thing", []), _da("b", "Thing", [])])
        got = vd.chapter_of(res)
        self.assertEqual(got["a"], (7, "Chapter 7"))
        self.assertEqual(got["b"], (None, "Other"))


class HeatmapTests(unittest.TestCase):
    def test_two_risk_types_count_in_both_but_once_in_total(self):
        res = _result([_da("1", "A", [
            _finding("F1", "High", risk_types=["Security", "Cost"]),
            _finding("F2", "Critical", risk_types=["Security"]),
        ])])
        (row,) = vd.heatmap_rows(res)
        self.assertEqual(row.cells["Security"], (2, "Critical"))
        self.assertEqual(row.cells["Cost"], (1, "High"))
        self.assertEqual(row.findings, 2)

    def test_distinct_counts_sum_to_total_findings(self):
        res = _result([
            _da("1", "A", [_finding("F1", risk_types=["Security", "Cost"]), _finding("F2")]),
            _da("2", "B", [_finding("F3", risk_types=["Availability"])]),
            _da("3", "C", []),
        ])
        rows = vd.heatmap_rows(res)
        self.assertEqual(sum(r.findings for r in rows),
                         sum(vd.severity_totals(res).values()))
        self.assertEqual([r.section_id for r in rows], ["1", "2"])

    def test_not_tagged_only_when_needed(self):
        tagged = _result([_da("1", "A", [_finding("F1", risk_types=["Cost"])])])
        self.assertEqual(vd.heatmap_columns(tagged), vd.RISK_TYPES)
        untagged = _result([_da("1", "A", [_finding("F1")])])
        self.assertEqual(vd.heatmap_columns(untagged), vd.RISK_TYPES + ["Not tagged"])
        self.assertEqual(vd.heatmap_rows(untagged)[0].cells, {"Not tagged": (1, "Medium")})

    def test_sap_red_or_yellow_section_without_findings_is_included(self):
        res = _result(
            [_da("1", "A", [_finding("F1")]), _da("2", "B", []), _da("3", "C", [])],
            coverage=[_cov("1", "1 A"), _cov("2", "2 B"), _cov("3", "3 C")],
            reconciliation=[_check("2", "RED"), _check("3", "GREEN")],
        )
        rows = vd.heatmap_rows(res)
        self.assertEqual([r.section_id for r in rows], ["1", "2"])
        self.assertEqual(rows[1].sap_rating, "RED")
        self.assertEqual(rows[1].findings, 0)
        self.assertIsNone(rows[0].sap_rating)

    def test_document_order_follows_coverage(self):
        res = _result(
            [_da("b", "B", [_finding("F1")]), _da("a", "A", [_finding("F2")])],
            coverage=[_cov("a", "1 A"), _cov("b", "2 B")],
        )
        self.assertEqual([r.section_id for r in vd.heatmap_rows(res)], ["a", "b"])

    def test_old_payload_does_not_crash(self):
        res = _result([_da("1", "A", [_finding("F1")])])
        (row,) = vd.heatmap_rows(res)
        self.assertIsNone(row.sap_rating)
        self.assertEqual(row.chapter, (None, "Other"))


class RealSampleTests(unittest.TestCase):
    def test_sample_payloads_if_present(self):
        out = Path(__file__).resolve().parents[1] / "output"
        for name in ("step20_d1_result.json", "step13_live_result.json"):
            path = out / name
            if not path.exists():
                continue
            res = AnalysisResult.model_validate_json(path.read_text(encoding="utf-8"))
            rows = vd.heatmap_rows(res)
            self.assertEqual(sum(r.findings for r in rows), sum(vd.severity_totals(res).values()))


if __name__ == "__main__":
    unittest.main()
