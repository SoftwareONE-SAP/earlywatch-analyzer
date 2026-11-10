"""The planner's reference_ids are cleaned before the analyst uses them."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ewa_pipeline.agents.orchestrator import _normalize_reference_ids
from ewa_pipeline.agents.skill_loader import SkillRegistry

SKILL = "ewa-analysis"
REGISTRY = SkillRegistry.from_dir(Path(__file__).resolve().parents[1] / "skills")


def normalize(ids, text="HANA memory"):
    return _normalize_reference_ids(REGISTRY, SKILL, ids, text)


class ReferenceNormalizerTests(unittest.TestCase):
    def test_unknown_id_is_dropped_and_warned(self):
        with self.assertLogs("ewa_pipeline.agents.orchestrator", level="WARNING") as logs:
            result = normalize(["thresholds-hana", "no-such-guide"])
        self.assertEqual(result, ["core-analysis", "thresholds-hana"])
        self.assertIn("no-such-guide", "\n".join(logs.output))

    def test_core_analysis_is_added_first(self):
        self.assertEqual(normalize(["remediation-hana", "thresholds-hana"])[0], "core-analysis")

    def test_core_analysis_moves_to_front_when_listed_later(self):
        self.assertEqual(normalize(["thresholds-hana", "core-analysis"]),
                         ["core-analysis", "thresholds-hana"])

    def test_empty_list_falls_back_to_suggestions(self):
        suggested = REGISTRY.suggest_references(SKILL, "HANA memory")
        result = normalize([], "HANA memory")
        self.assertEqual(result[0], "core-analysis")
        for ref_id in suggested:
            if ref_id not in {"thresholds", "remediation-patterns"}:
                self.assertIn(ref_id, result)

    def test_duplicates_removed_and_case_stripped(self):
        self.assertEqual(normalize([" Thresholds-HANA ", "thresholds-hana", "core-analysis"]),
                         ["core-analysis", "thresholds-hana"])

    def test_compat_indexes_are_removed(self):
        result = normalize(["thresholds", "remediation-patterns", "correlations"])
        self.assertNotIn("thresholds", result)
        self.assertNotIn("remediation-patterns", result)
        self.assertEqual(result, ["core-analysis", "correlations"])


if __name__ == "__main__":
    unittest.main()
