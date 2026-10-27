from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ewa_pipeline.agents.orchestrator import (  # noqa: E402
    _normalise_finding_ids,
    clean_evidence,
)
from ewa_pipeline.report.schemas import DomainAnalysis, Finding, Remediation  # noqa: E402

RAW = (
    "0118, columns: Statement Hash; Total Elapsed Time [s]; Number of Executions; "
    "Time / Execution [us]; Records / Execution; Time / Record [us]:\n"
    "<tr><td>b61a4a7ff31225a908196ac2ff49392b</td><td>1.056,2</td><td>169</td>"
    "<td>6.249.813,4</td><td>0,8</td><td>8.001.655,0</td></tr>\n"
    '0119: "FROM "SYS"."M_CS_UNLOADS" AS u JOIN "SYS"."M_CS_TABLES" AS t"\n'
    "0120, Thread State; Area; Samples:\n"
    "<tr><td>Running</td><td>SQL</td><td>59</td></tr>"
    "<tr><td>Job Exec Waiting</td><td>Idle</td><td>33</td></tr>\n"
    '0121: "[IMAGE]"'
)


class CleanEvidenceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.cleaned = clean_evidence(RAW)
        self.lines = self.cleaned.splitlines()

    def test_no_tags_remain(self) -> None:
        self.assertNotIn("<", self.cleaned)
        self.assertNotIn("</", self.cleaned)

    def test_rows_become_pipe_joined_lines(self) -> None:
        self.assertIn(
            "b61a4a7ff31225a908196ac2ff49392b | 1.056,2 | 169 | 6.249.813,4 | 0,8 | 8.001.655,0",
            self.lines,
        )
        self.assertIn("Running | SQL | 59", self.lines)
        self.assertIn("Job Exec Waiting | Idle | 33", self.lines)

    def test_source_id_prefixes_removed(self) -> None:
        for line in self.lines:
            self.assertFalse(line[:4].isdigit() and line[4:5] in ",:", line)
        self.assertFalse(any(line.startswith("0118") for line in self.lines))
        self.assertIn('"FROM "SYS"."M_CS_UNLOADS" AS u JOIN "SYS"."M_CS_TABLES" AS t"', self.lines)

    def test_image_lines_dropped(self) -> None:
        self.assertNotIn("[IMAGE]", self.cleaned)

    def test_labelled_image_placeholder_dropped(self) -> None:
        self.assertEqual(
            "Load is high [RED]",
            clean_evidence('Load is high [RED]\nRelated sources 0153 and 0158: "[IMAGE]"'),
        )

    def test_image_placeholder_next_to_text_kept(self) -> None:
        line = 'Chart: "[IMAGE]" shows 80% CPU'
        self.assertEqual(line, clean_evidence(line))

    def test_header_text_kept(self) -> None:
        self.assertIn("columns: Statement Hash; Total Elapsed Time [s]", self.cleaned)
        self.assertIn("Thread State; Area; Samples:", self.cleaned)

    def test_plain_text_unchanged_and_idempotent(self) -> None:
        plain = 'CPU 91 % [RED]\nMemory: 1.056,2 MB "ok"'
        self.assertEqual(plain, clean_evidence(plain))
        self.assertEqual(self.cleaned, clean_evidence(self.cleaned))

    def test_red_token_kept(self) -> None:
        self.assertEqual("[RED] Disk full: 98 %", clean_evidence("0042: [RED] Disk full: 98 %"))

    def test_entities_unescaped_and_blank_runs_collapsed(self) -> None:
        self.assertEqual("a & b\n\nc", clean_evidence("a &amp; b  \n\n\n\nc\n"))

    def test_orchestrator_cleans_finding_evidence(self) -> None:
        analysis = DomainAnalysis(
            section_title="S",
            section_id="0031",
            findings=[
                Finding(
                    id="F001",
                    title="Example",
                    severity="Medium",
                    description="Observed issue",
                    evidence=RAW,
                    impact="Potential delay",
                    remediation=Remediation(
                        action="Validate",
                        sap_transactions=["ST03N"],
                        effort_estimate="Low",
                        priority="Short-term",
                    ),
                )
            ],
            overall_health="Warning",
        )
        result = _normalise_finding_ids(analysis)
        self.assertEqual(self.cleaned, result.findings[0].evidence)
        self.assertNotIn("<tr>", result.findings[0].evidence)


if __name__ == "__main__":
    unittest.main()
