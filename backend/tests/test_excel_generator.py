"""The Excel workbook has an All Findings tab and keeps the section-sheet layout."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from openpyxl import load_workbook

from ewa_pipeline.report.excel_generator import generate
from ewa_pipeline.report.schemas import (
    AnalysisResult, DomainAnalysis, Finding, ReconciliationRow, Remediation, SectionCoverage,
)
from ewa_pipeline.tracking.token_tracker import TokenUsage


def _remediation(action: str) -> Remediation:
    return Remediation(
        action=action,
        sap_transactions=["SPAM"],
        effort_estimate="Medium",
        priority="Short-term",
    )


def old_style_finding() -> Finding:
    """Shaped like a finding saved before the new fields existed."""
    return Finding(
        id="F-001",
        title="Kernel release out of maintenance",
        severity="Medium",
        description="The kernel is old.",
        evidence="Kernel 753 [RED]",
        impact="No security patches.",
        remediation=_remediation("Upgrade the kernel."),
    )


def new_style_finding() -> Finding:
    return Finding(
        id="F-002",
        title="Expensive SQL statement",
        severity="Critical",
        description="One statement dominates database time.",
        evidence="Statement hash 4f3a9c uses 61% of DB time",
        impact="Slow dialog response.",
        remediation=_remediation("Tune the statement."),
        confidence="High",
        confidence_reason="The report rates it RED.",
        to_confirm="Check ST04 / DBACOCKPIT.",
        risk_types=["Performance", "Cost"],
        subject="4f3a9c",
        due_date="2026-12-31",
    )


def build_result() -> AnalysisResult:
    return AnalysisResult(
        domain_analyses=[
            DomainAnalysis(
                section_title="Software Configuration",
                section_id="1",
                findings=[old_style_finding()],
                overall_health="Warning",
            ),
            DomainAnalysis(
                section_title="Performance Indicators",
                section_id="2",
                findings=[new_style_finding()],
                overall_health="Critical",
            ),
        ],
        cross_references=[],
        executive_summary="Summary.",
        overall_system_health="Critical",
        top_5_priority_actions=["Tune the statement."],
        token_usage=TokenUsage(),
    )


def _headers(ws, row: int) -> list:
    return [c.value for c in ws[row]]


class ExcelGeneratorTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        path = Path(self._tmp.name) / "out.xlsx"
        generate(build_result(), path)
        self.wb = load_workbook(path)

    def test_all_findings_follows_executive_summary(self):
        names = self.wb.sheetnames
        self.assertEqual(names[0], "Executive Summary")
        self.assertEqual(names[1], "All Findings")
        for expected in ("Software Configuration", "Performance Indicators", "Remediation Plan", "Token Usage"):
            self.assertIn(expected, names)

    def test_all_findings_rows_sorted_by_severity(self):
        ws = self.wb["All Findings"]
        headers = _headers(ws, 1)
        self.assertEqual(headers[:3], ["Finding ID", "Section", "Severity"])
        self.assertIn("Observed (from report)", headers)
        self.assertIn("Interpretation", headers)
        self.assertEqual(ws.max_row, 3)  # header + exactly 2 findings

        rows = [dict(zip(headers, [c.value for c in ws[r]])) for r in (2, 3)]
        self.assertEqual([r["Severity"] for r in rows], ["Critical", "Medium"])

        new, old = rows
        self.assertEqual(new["Finding ID"], "F-002")
        self.assertEqual(new["Section"], "Performance Indicators")
        self.assertEqual(new["Risk Type"], "Performance, Cost")
        self.assertEqual(new["Confidence"], "High")
        self.assertEqual(new["Why this confidence"], "The report rates it RED.")
        self.assertEqual(new["To confirm"], "Check ST04 / DBACOCKPIT.")
        self.assertEqual(new["Observed (from report)"], "Statement hash 4f3a9c uses 61% of DB time")
        self.assertEqual(new["Interpretation"], "One statement dominates database time.")
        self.assertEqual(new["Due date"], "2026-12-31")

        # Old-style finding: new fields render as empty cells.
        self.assertIn(old["Risk Type"], ("", None))
        self.assertIn(old["Confidence"], ("", None))
        self.assertIn(old["To confirm"], ("", None))
        self.assertEqual(old["Observed (from report)"], "Kernel 753 [RED]")

    def test_finding_id_links_to_section_sheet(self):
        ws = self.wb["All Findings"]
        # Same "#'Sheet'!A1" style the Executive Summary already uses.
        target = ws["A2"].hyperlink.target or ws["A2"].hyperlink.location
        self.assertEqual(target, "#'Performance Indicators'!A3")

    def test_section_sheet_layout_kept_for_summary_formulas(self):
        ws = self.wb["Software Configuration"]
        self.assertEqual(ws["A3"].value, "F-001")
        self.assertEqual(ws["B3"].value, "Medium")
        headers = _headers(ws, 2)
        self.assertEqual(headers[:2], ["ID", "Severity"])
        self.assertIn("Observed (from report)", headers)
        self.assertIn("Interpretation", headers)
        self.assertNotIn("Evidence", headers)
        self.assertNotIn("Description", headers)
        self.assertEqual(headers[-3:], ["Confidence", "Risk Type", "To confirm"])

    def test_section_sheet_shows_new_fields(self):
        ws = self.wb["Performance Indicators"]
        headers = _headers(ws, 2)
        row = dict(zip(headers, [c.value for c in ws[3]]))
        self.assertEqual(row["Confidence"], "High")
        self.assertEqual(row["Risk Type"], "Performance, Cost")
        self.assertEqual(row["To confirm"], "Check ST04 / DBACOCKPIT.")

    def test_executive_summary_formulas_still_use_columns_a_and_b(self):
        ws = self.wb["Executive Summary"]
        formulas = [
            str(c.value) for row in ws.iter_rows() for c in row
            if isinstance(c.value, str) and c.value.startswith("=")
        ]
        self.assertTrue(any("$A$3:$A$9999" in f and "COUNTA" in f for f in formulas))
        self.assertTrue(any("B$3:$B$9999" in f or "B3:B9999" in f.replace("$", "") for f in formulas))

    def test_section_named_all_findings_does_not_collide(self):
        result = build_result()
        result.domain_analyses[0].section_title = "All Findings"
        path = Path(self._tmp.name) / "collide.xlsx"
        generate(result, path)
        names = load_workbook(path).sheetnames
        self.assertEqual(len(names), len(set(names)))
        self.assertEqual(names[1], "All Findings")


def _row(source, verdict, **kw) -> ReconciliationRow:
    return ReconciliationRow(source=source, verdict=verdict, **kw)


class SapVsUsTests(unittest.TestCase):
    def _generate(self, result):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        path = Path(tmp.name) / "out.xlsx"
        generate(result, path)
        return load_workbook(path)

    def test_sap_vs_us_sheet_position_rows_and_counts(self):
        result = build_result()
        result.reconciliation = [
            _row("Alert", "Agree", sap_topic="Alerts", sap_item="Kernel old", sap_rating="RED",
                 our_section_id="1", our_section_title="Software Configuration",
                 our_rating="RED", finding_ids=["F-001", "F-003"], match_score=0.8),
            _row("Alert", "Not covered", sap_item="Odd alert", sap_rating="YELLOW"),
            _row("Check", "Agree", sap_topic="Performance", sap_rating="GREEN", our_rating="GREEN"),
            _row("Check", "We rated higher", sap_topic="Hardware", sap_rating="YELLOW", our_rating="RED"),
        ]
        wb = self._generate(result)
        self.assertEqual(wb.sheetnames[:3], ["Executive Summary", "All Findings", "SAP vs Us"])
        ws = wb["SAP vs Us"]

        counts = {ws.cell(r, 1).value: (ws.cell(r, 2).value, ws.cell(r, 3).value, ws.cell(r, 4).value)
                  for r in range(3, 6)}
        self.assertEqual(counts["Agree"], (1, 1, 2))
        self.assertEqual(counts["Not covered"], (1, 0, 1))
        self.assertEqual(counts["We rated higher"], (0, 1, 1))

        hdr_row = next(r for r in range(1, 15) if ws.cell(r, 1).value == "Source")
        headers = _headers(ws, hdr_row)
        self.assertEqual(headers[:4], ["Source", "SAP Topic", "SAP Item", "SAP Rating"])
        self.assertEqual(ws.max_row - hdr_row, 4)  # one row per reconciliation row
        first = dict(zip(headers, [c.value for c in ws[hdr_row + 1]]))
        self.assertEqual(first["Our Finding IDs"], "F-001, F-003")
        self.assertEqual(first["Verdict"], "Agree")
        self.assertEqual(first["Match score"], 0.8)
        self.assertEqual(ws.freeze_panes, f"A{hdr_row + 1}")

    def test_verified_healthy_rows_and_sap_disagrees(self):
        result = build_result()  # sections "1" and "2" have findings
        result.coverage = [
            SectionCoverage(section_id="1", section_title="Software Configuration", status="analyzed"),
            SectionCoverage(section_id="3", section_title="Hardware", status="analyzed"),
            SectionCoverage(section_id="4", section_title="Database", status="analyzed"),
            SectionCoverage(section_id="5", section_title="Security", status="failed"),
        ]
        result.reconciliation = [
            _row("Check", "Not covered", sap_topic="Database", sap_rating="YELLOW", our_section_id="4"),
            _row("Check", "Agree", sap_topic="Database", sap_rating="RED", our_section_id="4"),
        ]
        wb = self._generate(result)
        ws = wb["No Issues Found"]
        self.assertEqual(ws.max_row, 3)  # header + 2 healthy sections
        rows = {ws.cell(r, 1).value: (ws.cell(r, 2).value, ws.cell(r, 3).value) for r in (2, 3)}
        self.assertFalse(any(rows["3 Hardware"]))
        self.assertEqual(rows["4 Database"], ("RED", "SAP disagrees"))
        self.assertEqual(sum(1 for _, n in rows.values() if n == "SAP disagrees"), 1)

    def test_both_sheets_ordered_when_both_present(self):
        result = build_result()
        result.coverage = [SectionCoverage(section_id="9", section_title="Clean", status="analyzed")]
        result.reconciliation = [_row("Check", "Agree", sap_rating="GREEN")]
        names = self._generate(result).sheetnames
        self.assertEqual(names[1:4], ["All Findings", "SAP vs Us", "No Issues Found"])

    def test_old_payload_has_neither_sheet(self):
        wb = self._generate(build_result())
        self.assertNotIn("Verified Healthy", wb.sheetnames)
        self.assertNotIn("SAP vs Us", wb.sheetnames)
        self.assertNotIn("No Issues Found", wb.sheetnames)

    def test_coverage_without_healthy_sections_skips_sheet(self):
        result = build_result()
        result.coverage = [SectionCoverage(section_id="1", section_title="Software Configuration",
                                           status="analyzed")]
        self.assertNotIn("No Issues Found", self._generate(result).sheetnames)


def _finding(fid: str, severity: str) -> Finding:
    return Finding(
        id=fid, title=f"Finding {fid}", severity=severity,
        description="d", evidence="e", impact="i", remediation=_remediation("Fix."),
    )


class WorstSeverityTests(unittest.TestCase):
    def _summary_rows(self, result):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        path = Path(tmp.name) / "out.xlsx"
        generate(result, path)
        ws = load_workbook(path)["Executive Summary"]
        hdr = next(r for r in ws.iter_rows() if r[2].value == "Worst severity")
        rows = []
        for r in range(hdr[0].row + 1, ws.max_row + 1):
            if ws.cell(row=r, column=2).value:
                rows.append((ws.cell(row=r, column=2).value, ws.cell(row=r, column=3).value,
                             ws.cell(row=r, column=3).fill.fgColor.rgb))
        return rows

    def test_worst_severity_and_sorting(self):
        result = build_result()
        # Medium-only section listed first, but labelled "Healthy" by the AI.
        result.domain_analyses = [
            DomainAnalysis(section_title="Mild", section_id="1", overall_health="Healthy",
                           findings=[_finding("M-1", "Medium"), _finding("M-2", "Low")]),
            DomainAnalysis(section_title="Serious", section_id="2", overall_health="Healthy",
                           findings=[_finding("H-1", "Low"), _finding("H-2", "High")]),
        ]
        rows = self._summary_rows(result)
        self.assertEqual([r[0] for r in rows], ["Serious", "Mild"])
        self.assertEqual([r[1] for r in rows], ["High", "Medium"])
        self.assertTrue(rows[1][2].endswith("FFC000"))

    def test_ties_sorted_by_finding_count(self):
        result = build_result()
        result.domain_analyses = [
            DomainAnalysis(section_title="One", section_id="1", overall_health="Warning", findings=[_finding("A-1", "High")]),
            DomainAnalysis(section_title="Two", section_id="2", overall_health="Warning",
                           findings=[_finding("B-1", "High"), _finding("B-2", "Low")]),
        ]
        self.assertEqual([r[0] for r in self._summary_rows(result)], ["Two", "One"])


if __name__ == "__main__":
    unittest.main()
