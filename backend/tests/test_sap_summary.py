from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ewa_pipeline.indexer.sap_summary import extract_service_summary  # noqa: E402

REPO = Path(__file__).resolve().parents[2]
COREX = REPO / "samples" / "COREX_TP1_05_2026_files_html" / "COREX_TP1_05_2026.htm"
BSW = REPO / "samples" / "compare" / "lo_test" / "BSW_S4P_05_2026.xml"

TD_ONLY = """
<p>Alert Overview</p>
<table>
<tr><td><span data-rating="red">[RED]</span></td><td>Some alert</td><td>Alert text one</td></tr>
<tr><td></td><td>No rating here</td></tr>
<tr><td>[YELLOW]</td><td>Alert text two</td></tr>
</table>
<p>Check Overview</p>
<table>
<tr><td>Topic Rating</td><td>Topic</td><td>Subtopic Rating</td><td>Subtopic</td></tr>
<tr><td>[YELLOW]</td><td>Performance *</td><td>[RED]</td><td>SQL Statements *</td></tr>
<tr><td></td><td></td><td>[GREEN]</td><td>Memory</td></tr>
<tr><td>[GREEN]</td><td>Security</td><td></td><td></td></tr>
</table>
"""

TH_FIRST = """
<p>Alert Overview</p>
<table>
<tr><th>[RED]</th><th>First alert</th></tr>
<tr><td>[GREEN]</td><td>Second alert</td></tr>
</table>
"""


def _counts(items):
    return dict(Counter(i.rating for i in items))


class UnitTests(unittest.TestCase):
    def test_td_only_alerts_skip_rows_without_rating(self):
        result = extract_service_summary(TD_ONLY)
        self.assertEqual([(a.rating, a.text) for a in result.alerts],
                         [("RED", "Alert text one"), ("YELLOW", "Alert text two")])

    def test_th_first_row_is_read(self):
        result = extract_service_summary(TH_FIRST)
        self.assertEqual([(a.rating, a.text) for a in result.alerts],
                         [("RED", "First alert"), ("GREEN", "Second alert")])

    def test_checks_topics_subtopics_and_star_stripping(self):
        checks = extract_service_summary(TD_ONLY).checks
        self.assertEqual(
            [(c.topic, c.subtopic, c.rating, c.raw_title) for c in checks],
            [
                ("Performance", "", "YELLOW", "Performance *"),
                ("Performance", "SQL Statements", "RED", "SQL Statements *"),
                ("Performance", "Memory", "GREEN", "Memory"),
                ("Security", "", "GREEN", "Security"),
            ],
        )

    def test_only_one_trailing_star_is_stripped(self):
        html = "<p>Check Overview</p><table><tr><td>[RED]</td><td>A * *</td><td></td><td></td></tr></table>"
        check = extract_service_summary(html).checks[0]
        self.assertEqual((check.topic, check.raw_title), ("A *", "A * *"))

    def test_missing_sections_give_empty_lists(self):
        for html in ("", "<p>Nothing here</p>", "<p>Alert Overview</p>", "<p>Check Overview</p><p>x</p>"):
            result = extract_service_summary(html)
            self.assertEqual((result.alerts, result.checks), ([], []))


class SampleTests(unittest.TestCase):
    def _check_counts(self, summary, alerts, topics, subtopics):
        self.assertEqual(_counts(summary.alerts), alerts)
        self.assertEqual(_counts([c for c in summary.checks if not c.subtopic]), topics)
        self.assertEqual(_counts([c for c in summary.checks if c.subtopic]), subtopics)

    def test_corex_sample(self):
        if not COREX.is_file():
            self.skipTest("COREX sample missing")
        from converters.compact_html_converter import convert_html_to_compact_html
        with tempfile.TemporaryDirectory() as tmp:
            compact = convert_html_to_compact_html(COREX, Path(tmp) / "corex.compact.html")
        self._check_counts(
            extract_service_summary(compact),
            {"RED": 4, "YELLOW": 7},
            {"RED": 1, "YELLOW": 3, "GREEN": 4},
            {"RED": 4, "YELLOW": 10, "GREEN": 24},
        )

    def test_bsw_sample(self):
        if not BSW.is_file():
            self.skipTest("BSW sample missing")
        from converters.compact_html_converter import convert_html_to_compact_html
        from converters.doc_html_converter import convert_doc_to_html
        with tempfile.TemporaryDirectory() as tmp:
            doc = Path(tmp) / "BSW_S4P_05_2026.doc"
            shutil.copy(BSW, doc)
            html_path = convert_doc_to_html(doc, Path(tmp) / "out")
            compact = convert_html_to_compact_html(html_path, Path(tmp) / "bsw.compact.html")
        self._check_counts(
            extract_service_summary(compact),
            {"RED": 4, "YELLOW": 6},
            {"RED": 1, "YELLOW": 8, "GREEN": 3},
            {"RED": 3, "YELLOW": 15, "GREEN": 37},
        )


if __name__ == "__main__":
    unittest.main()
