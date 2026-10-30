"""Tests for the interactive HTML explorer: data builder and page rendering."""
from __future__ import annotations

import json
import re
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ewa_pipeline.report.excel_generator import _findings_in_order
from ewa_pipeline.report.explorer_html import (
    FINDING_COLUMNS, build_explorer_data, render_explorer_html, write_explorer,
)
from test_excel_generator import build_result
from test_excel_whole_workbook import full_result


def _embedded_data(html: str) -> dict:
    """Read the JSON back out of the page (undoing the "<" escape)."""
    m = re.search(r"const DATA = (\{.*?\});\n", html, re.S)
    assert m, "no DATA object in page"
    return json.loads(m.group(1))


class ExplorerHtmlTests(unittest.TestCase):
    def test_placeholder_replaced(self):
        html = render_explorer_html(build_explorer_data(full_result(), "src"))
        self.assertNotIn("/*__DATA__*/null", html)
        self.assertIn("const DATA = {", html)

    def test_script_tag_in_finding_title_is_escaped(self):
        result = full_result()
        result.domain_analyses[0].findings[0].title = "</script><script>alert(1)</script>"
        html = render_explorer_html(build_explorer_data(result, "src"))
        self.assertNotIn("</script><script>alert(1)", html)
        titles = [f["Title"] for f in _embedded_data(html)["findings"]]
        self.assertIn("</script><script>alert(1)</script>", titles)

    def test_no_reconciliation_gives_empty_compare(self):
        data = build_explorer_data(build_result(), "src")
        self.assertEqual(data["compare"]["rows"], [])
        self.assertEqual(data["compare"]["summary"], [])
        render_explorer_html(data)

    def test_zero_findings_renders(self):
        result = build_result()
        for da in result.domain_analyses:
            da.findings = []
        data = build_explorer_data(result, "src")
        self.assertEqual(data["findings"], [])
        self.assertEqual(data["heatmap"]["rows"], [])
        self.assertIn("const DATA = {", render_explorer_html(data))

    def test_findings_match_excel_order(self):
        result = full_result()
        data = build_explorer_data(result, "src")
        expected = [f.id for _da, f in _findings_in_order(result)]
        self.assertEqual([f["Ref."] for f in data["findings"]], expected)
        self.assertEqual(list(data["findings"][0]), FINDING_COLUMNS)
        self.assertEqual(len(FINDING_COLUMNS), 19)
        self.assertEqual(data["findings"][0]["Severity"], "Critical")
        self.assertEqual(data["findings"][0]["Risk area"], "Performance, Cost")

    def test_extra_heatmap_column_flows_through(self):
        result = full_result()
        result.domain_analyses[0].findings[0].risk_types = []  # becomes "Not tagged"
        heat = build_explorer_data(result, "src")["heatmap"]
        self.assertIn("Not tagged", heat["risks"])
        self.assertTrue(heat["rows"])
        for row in heat["rows"]:
            self.assertEqual(len(row["cells"]), len(heat["risks"]))
        self.assertEqual(heat["rows"][-1]["section"], "Total")

    def test_header_fields_actions_and_combos(self):
        data = build_explorer_data(full_result(), "src")
        self.assertEqual(data["sid"], "PRD")
        self.assertEqual(data["health"], "CRITICAL")
        self.assertEqual(data["source"], "src")
        self.assertEqual(data["actions"][0]["refs"], ["F-002", "F-001"])
        self.assertEqual(data["combos"][0]["refs"], ["F-001", "F-002"])
        self.assertIn("What to do: Fix both.", data["combos"][0]["body"])
        self.assertEqual(len(data["compare"]["rows"]), 2)
        self.assertEqual(len(data["compare"]["rows"][0]), 14)

    def test_write_explorer(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = write_explorer(full_result(), Path(tmp) / "sub" / "x.html", "src")
            self.assertTrue(path.read_text(encoding="utf-8").startswith("<!doctype html>"))


class ExplorerSafeWriteTests(unittest.TestCase):
    def test_failure_returns_none(self):
        from unittest.mock import patch
        from ewa_pipeline.services import pipeline
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(pipeline.explorer_html, "write_explorer", side_effect=RuntimeError("boom")):
                out = pipeline._write_explorer_safely(full_result(), Path(tmp) / "a_workbook.xlsx", "src")
        self.assertIsNone(out)

    def test_success_returns_path(self):
        from ewa_pipeline.services import pipeline
        with tempfile.TemporaryDirectory() as tmp:
            out = pipeline._write_explorer_safely(full_result(), Path(tmp) / "a_workbook.xlsx", "src")
            self.assertEqual(out.name, "a_workbook_explorer.html")
            self.assertTrue(out.exists())


if __name__ == "__main__":
    unittest.main()
