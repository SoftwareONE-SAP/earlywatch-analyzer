"""Grouped planning contracts with synthetic source sections only."""
from __future__ import annotations

import unittest

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from ewa_pipeline.agents.planning import prepare_sections, validate_plan, parent_context, planning_catalogue
from ewa_pipeline.config import Config
from ewa_pipeline.indexer.tree_navigator import get_analyzable_sections
from ewa_pipeline.report.schemas import OrchestratorPlan, SectionPlanItem
from test_cli_analysis_settings import configured
CONFIG = configured()


def plan(*groups):
    return OrchestratorPlan(tasks=[SectionPlanItem(section_ids=list(ids), section_title="Database review",
        analysis_focus="Compare related SQL measurements.") for ids in groups])


def sources():
    return [
        {"id": "0001", "title": "Database", "branch_id": "0001", "ancestor_ids": [], "content_chars": 10},
        {"id": "0002", "title": "SQL A", "branch_id": "0001", "ancestor_ids": ["0001"], "content_chars": 20},
        {"id": "0003", "title": "SQL B", "branch_id": "0001", "ancestor_ids": ["0001"], "content_chars": 20},
        {"id": "0004", "title": "Security", "branch_id": "0004", "ancestor_ids": [], "content_chars": 10},
    ]


class GroupingTests(unittest.TestCase):
    def assert_partition(self, tasks, ids):
        actual = [sid for task in tasks for sid in task["section_ids"]]
        self.assertCountEqual(actual, ids)
        self.assertEqual(len(actual), len(set(actual)))

    def test_planner_groups_related_sources_and_preserves_priority(self):
        tasks, origins, _ = validate_plan(plan(["0004"], ["0001", "0002", "0003"]), sources(), CONFIG)
        self.assertEqual([task["section_ids"] for task in tasks], [["0004"], ["0001", "0002", "0003"]])
        self.assert_partition(tasks, [s["id"] for s in sources()])
        self.assertEqual(set(origins.values()), {"planner"})

    def test_fallback_groups_by_hierarchy_instead_of_one_task_per_heading(self):
        tasks, _, _ = validate_plan(None, sources(), CONFIG)
        self.assertEqual([t["section_ids"] for t in tasks], [["0001", "0002", "0003"], ["0004"]])

    def test_unknown_duplicate_and_overlapping_ids_cannot_lose_sources(self):
        tasks, _, notes = validate_plan(plan(["0002", "unknown"], ["0001", "0001"],
            ["0002", "0003"], ["0003", "0004"]), sources(), CONFIG)
        self.assert_partition(tasks, [s["id"] for s in sources()])
        self.assertTrue(notes)
        self.assertIn(["0002", "0003"], [t["section_ids"] for t in tasks])

    def test_source_budgets_split_groups_without_truncating_or_dropping(self):
        config = CONFIG.model_copy(update={"max_task_sections": 2, "max_task_content_chars": 30})
        tasks, _, _ = validate_plan(plan([s["id"] for s in sources()]), sources(), config)
        self.assert_partition(tasks, [s["id"] for s in sources()])
        self.assertTrue(all(t["source_content_chars"] <= 30 for t in tasks))
        self.assertTrue(all(len(t["section_ids"]) <= 2 for t in tasks))

    def test_oversized_single_source_is_flagged_and_never_truncated(self):
        config = CONFIG.model_copy(update={"max_task_content_chars": 5})
        tasks, _, _ = validate_plan(None, sources(), config)
        self.assert_partition(tasks, [s["id"] for s in sources()])
        self.assertTrue(all(t["oversized"] for t in tasks))

    def test_heading_only_parent_context_survives_source_discovery(self):
        tree = {"structure": [{"node_id": "0001", "title": "Database", "text": "<h1>Database</h1>",
            "nodes": [{"node_id": "0002", "title": "SQL A", "text": "<h2>SQL A</h2><p>SQL A runtime 95%</p>", "nodes": []}]}]}
        nodes = get_analyzable_sections(tree)
        sections, contexts = prepare_sections(tree, nodes, {n.id: n.content for n in nodes})
        self.assertEqual(sections[0]["parent_id"], "0001")
        self.assertEqual(sections[0]["branch_id"], "0001")
        catalogue = planning_catalogue(sections, contexts)
        self.assertEqual(len(catalogue), 2)
        self.assertFalse(catalogue[0]["source"])
        self.assertEqual(catalogue[1]["parent"], "0001")
        self.assertTrue(catalogue[1]["source"])
        text, ids = parent_context(["0002"], sections, contexts, 200)
        self.assertIn("Database", text)
        self.assertEqual(ids, ["0001"])
        bounded, _ = parent_context(["0002"], sections, contexts, 10)
        self.assertLessEqual(len(bounded), 10)
        self.assertEqual(parent_context(["0002"], sections, contexts, 0), ("", []))

    def test_split_groups_keep_parent_context_separate_from_owned_sources(self):
        sections = sources()
        config = CONFIG.model_copy(update={"max_task_sections": 2})
        tasks, _, _ = validate_plan(plan(["0001", "0002", "0003"]), sections, config)
        text, ids = parent_context(tasks[1]["section_ids"], sections, {"0001": "Database parent metric 95%"}, 200)
        self.assertEqual(tasks[1]["section_ids"], ["0003"])
        self.assertIn("Database parent metric 95%", text)
        self.assertEqual(ids, ["0001"])
        self.assertNotIn("0001", tasks[1]["section_ids"])


if __name__ == "__main__":
    unittest.main()
