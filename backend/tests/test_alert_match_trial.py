"""Offline alert-matching trial: no network, fake Decision-1 answers."""
from __future__ import annotations

import csv
import json
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from click.testing import CliRunner

from ewa_pipeline.agents.decision_client import decide
from ewa_pipeline.main import cli
from ewa_pipeline.report import alert_match_trial as T
from test_decision_client import FakePost, make_config, ok


def finding(fid, title, evidence="", severity="High"):
    return {
        "id": fid, "title": title, "severity": severity, "description": "d", "evidence": evidence,
        "impact": "i", "remediation": {"action": "a", "sap_transactions": [], "effort_estimate": "Low", "priority": "Immediate"},
    }


def make_result():
    return {
        "domain_analyses": [
            {"section_title": "Security", "section_id": "1", "overall_health": "Critical", "findings": [
                finding("S-1", "System replication network settings insecure", "x" * 2000),
                finding("S-2", "User SYSTEM is active"),
            ]},
            {"section_title": "Performance", "section_id": "2", "overall_health": "Warning", "findings": [
                finding("P-1", "Expensive SQL statements", severity="Medium"),
            ]},
        ],
        "cross_references": [], "executive_summary": "e", "overall_system_health": "Critical",
        "top_5_priority_actions": [], "token_usage": {},
        "sap_summary": {"alerts": [
            {"rating": "RED", "text": "SAP HANA network settings for System Replication is insecure."},
            {"rating": "RED", "text": "User SYSTEM is active and valid."},
            {"rating": "YELLOW", "text": "Backup is missing."},
        ], "checks": []},
    }


P = {"S-1": 0.97, "S-2": 0.6, "P-1": 0.1}


def fake_ask(question, options, context):
    p = P[context["finding"]["id"]]
    return {"true": p, "false": 1 - p}


class TrialTests(unittest.TestCase):
    def setUp(self):
        self.pairs = T.build_pairs(make_result())

    def test_pairs_cover_every_alert_and_finding_with_ranks(self):
        self.assertEqual(len(self.pairs), 9)
        first = [p for p in self.pairs if p["alert_no"] == 1]
        best = min(first, key=lambda p: p["jaccard_rank"])
        self.assertEqual(best["finding_id"], "S-1")
        self.assertEqual(sorted(p["jaccard_rank"] for p in first), [1, 2, 3])

    def test_state_cuts_evidence(self):
        state = T.pair_state(self.pairs[0])
        self.assertEqual(len(state["finding"]["evidence"]), 1500)
        self.assertEqual(state["sap_alert"]["rating"], "RED")
        self.assertEqual(state["finding"]["section"], "Security")

    def test_picks_and_bands(self):
        scores = T.score_pairs(self.pairs, fake_ask)
        wo = T.pick_word_overlap(self.pairs)
        self.assertEqual(wo[1]["finding_id"], "S-1")
        self.assertIsNone(wo[3])
        by_alert, by_pair = T.pick_decision(self.pairs, scores)
        self.assertEqual(by_alert[1]["pick"], "S-1")
        self.assertEqual(by_alert[1]["possibles"], ["S-2"])
        self.assertEqual(by_alert[1]["extra"], [])
        self.assertEqual(by_pair[(1, "S-1")]["verdict"], "match")
        self.assertEqual(by_pair[(1, "S-2")]["verdict"], "possible")
        self.assertEqual(by_pair[(1, "P-1")]["verdict"], "none")
        self.assertEqual(by_pair[(1, "S-2")]["rank"], 2)

    def test_extra_matches(self):
        scores = {(1, "S-1"): 0.95, (1, "S-2"): 0.85, (1, "P-1"): 0.2}
        by_alert, _ = T.pick_decision(self.pairs, scores)
        self.assertEqual(by_alert[1]["pick"], "S-1")
        self.assertEqual(by_alert[1]["extra"], ["S-2"])

    def test_errors_do_not_crash(self):
        scores = T.score_pairs(self.pairs, lambda q, o, c: {})
        self.assertTrue(all(v is None for v in scores.values()))
        by_alert, by_pair = T.pick_decision(self.pairs, scores)
        self.assertIsNone(by_alert[1]["pick"])
        self.assertEqual(by_pair[(1, "S-1")]["verdict"], "error")
        self.assertIsNone(by_pair[(1, "S-1")]["rank"])

    def test_scoreboard(self):
        wo = {1: {"finding_id": "S-1", "score": 0.5}, 2: {"finding_id": "P-1", "score": 0.4}, 3: None, 4: None}
        d1 = {
            1: {"pick": "S-1", "p": 0.9, "extra": ["S-2", "P-1"], "possibles": []},
            2: {"pick": None, "p": None, "extra": [], "possibles": []},
            3: {"pick": "S-2", "p": 0.9, "extra": [], "possibles": []},
            4: {"pick": None, "p": None, "extra": [], "possibles": []},
        }
        labels = {1: {"S-1", "S-2"}, 2: {"S-2"}, 3: set(), 4: set()}
        board = T.scoreboard(labels, wo, d1)
        self.assertEqual(board["word_overlap"], {"right": 1, "wrong": 1, "missed": 0, "correct_none": 2})
        self.assertEqual(board["decision"],
                         {"right": 1, "wrong": 1, "missed": 1, "correct_none": 1, "wrong_extras": 1})
        self.assertIn("Word overlap", T.format_scoreboard(board))

    def test_csvs_and_labels_roundtrip(self):
        scores = T.score_pairs(self.pairs, fake_ask)
        wo = T.pick_word_overlap(self.pairs)
        by_alert, by_pair = T.pick_decision(self.pairs, scores)
        with TemporaryDirectory() as tmp:
            pairs_csv, summary_csv = Path(tmp) / "p.csv", Path(tmp) / "s.csv"
            T.write_pairs_csv(pairs_csv, self.pairs, by_pair)
            T.write_summary_csv(summary_csv, self.pairs, wo, by_alert, scores)
            with open(pairs_csv, encoding="utf-8-sig") as f:
                self.assertEqual(len(list(csv.DictReader(f))), 9)
            with open(summary_csv, encoding="utf-8-sig") as f:
                rows = list(csv.DictReader(f))
            self.assertEqual(rows[0]["d1_pick"], "S-1")
            self.assertIn("S-1: System replication", rows[0]["top_candidates"])
            self.assertFalse(T.summary_has_labels(summary_csv))
            rows[0]["correct_finding_ids"] = "S-1; S-2"
            rows[1]["correct_finding_ids"] = "NONE"
            with open(summary_csv, "w", newline="", encoding="utf-8-sig") as f:
                w = csv.DictWriter(f, fieldnames=T.SUMMARY_COLUMNS)
                w.writeheader()
                w.writerows(rows)
            self.assertTrue(T.summary_has_labels(summary_csv))
            self.assertEqual(T.read_labels(summary_csv), {1: {"S-1", "S-2"}, 2: set()})

    def test_real_decide_request_body(self):
        post = FakePost(ok(0.9))
        config = make_config(decision_enabled=True)
        T.score_pairs(self.pairs[:1], lambda q, o, c: decide(q, o, c, config=config, post=post))
        body = post.calls[0][1]["json"]
        self.assertIn("System Replication", body["state"]["sap_alert"]["text"])
        self.assertTrue(body["state"]["finding"]["evidence"].startswith("xxx"))
        self.assertEqual(body["questions"]["answer"]["instructions"], T.QUESTION)


class CommandTests(unittest.TestCase):
    def run_cmd(self, args):
        config = make_config()
        with patch("ewa_pipeline.main._load_env_and_config", return_value=config):
            return CliRunner().invoke(cli, ["alert-trial", *args])

    def test_run_then_reuse_with_labels(self):
        calls = []

        def fake_decide(question, options, context, *, config, **kw):
            calls.append(1)
            self.assertTrue(config.decision_enabled)
            return fake_ask(question, options, context)

        with TemporaryDirectory() as tmp:
            result_path, prefix = Path(tmp) / "r.json", str(Path(tmp) / "out")
            result_path.write_text(json.dumps(make_result()), encoding="utf-8")
            with patch("ewa_pipeline.agents.decision_client.decide", fake_decide):
                res = self.run_cmd(["--result", str(result_path), "--out-prefix", prefix])
                self.assertEqual(res.exit_code, 0, res.output)
                self.assertEqual(len(calls), 9)
                for suffix in ("_d1_scores.json", "_alert_pairs.csv", "_alert_summary.csv"):
                    self.assertTrue(Path(prefix + suffix).exists(), suffix)

                summary = Path(prefix + "_alert_summary.csv")
                with open(summary, encoding="utf-8-sig") as f:
                    rows = list(csv.DictReader(f))
                rows[0]["correct_finding_ids"] = "S-1"
                with open(summary, "w", newline="", encoding="utf-8-sig") as f:
                    w = csv.DictWriter(f, fieldnames=T.SUMMARY_COLUMNS)
                    w.writeheader()
                    w.writerows(rows)

                calls.clear()
                res = self.run_cmd(["--result", str(result_path), "--out-prefix", prefix,
                                    "--reuse-scores", "--labels", str(summary)])
            self.assertEqual(res.exit_code, 0, res.output)
            self.assertEqual(calls, [])
            self.assertIn("Scoreboard", res.output)
            # the labelled file was backed up before the new summary was written
            backups = list(Path(tmp).glob("out_alert_summary_labelled_backup_*.csv"))
            self.assertEqual(len(backups), 1)
            self.assertEqual(T.read_labels(backups[0]), {1: {"S-1"}})

    def test_all_calls_failed_exits_non_zero(self):
        with TemporaryDirectory() as tmp:
            result_path = Path(tmp) / "r.json"
            result_path.write_text(json.dumps(make_result()), encoding="utf-8")
            with patch("ewa_pipeline.agents.decision_client.decide", lambda *a, **k: {}):
                res = self.run_cmd(["--result", str(result_path), "--out-prefix", str(Path(tmp) / "o")])
            self.assertNotEqual(res.exit_code, 0)
            self.assertIn("every call failed", res.output.lower())


if __name__ == "__main__":
    unittest.main()
