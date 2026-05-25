from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ewa_pipeline.agents.prompts import (  # noqa: E402
    DOMAIN_ANALYST_PROMPT,
    ORCHESTRATOR_PLANNING_PROMPT,
)
from ewa_pipeline.agents.skill_loader import SkillRegistry  # noqa: E402


SKILLS_DIR = Path(__file__).resolve().parents[1] / "skills"


class SkillLoaderTests(unittest.TestCase):
    def _registry(self) -> SkillRegistry:
        return SkillRegistry.from_dir(SKILLS_DIR)

    def test_catalog_lists_references_without_reference_bodies(self) -> None:
        catalog = self._registry().catalog_text()

        self.assertIn("skill_name: ewa-analysis", catalog)
        self.assertIn("thresholds-memory", catalog)
        self.assertNotIn("Extended memory utilization | < 80%", catalog)

    def test_resolve_context_loads_only_selected_references(self) -> None:
        context = self._registry().resolve_context(
            "ewa-analysis",
            ["thresholds-memory"],
        )

        self.assertIn("SAP EarlyWatch Alert Analysis", context)
        self.assertIn("Extended memory utilization", context)
        self.assertNotIn("Users with SAP_ALL in production", context)

    def test_invalid_skill_and_reference_ids_fall_back_safely(self) -> None:
        registry = self._registry()

        missing_skill = registry.resolve_context(
            "unknown-skill",
            ["thresholds-memory"],
            fallback_text="fallback",
        )
        invalid_reference = registry.resolve_context(
            "ewa-analysis",
            ["unknown-reference"],
            fallback_text="fallback",
        )

        self.assertEqual("fallback", missing_skill)
        self.assertIn("SAP EarlyWatch Alert Analysis", invalid_reference)
        self.assertNotIn("Extended memory utilization", invalid_reference)

    def test_prompts_separate_catalog_from_loaded_skill_context(self) -> None:
        registry = self._registry()
        catalog = registry.catalog_text()
        skill_context = registry.resolve_context("ewa-analysis", ["thresholds-memory"])

        planner_prompt = ORCHESTRATOR_PLANNING_PROMPT.format(
            tree_summary="id=001 Memory Overview",
            sections="id=001 | SAP Memory: summary",
            skills_catalog=catalog,
        )
        domain_prompt = DOMAIN_ANALYST_PROMPT.format(
            section_title="SAP Memory",
            section_id="001",
            analysis_focus="Check memory thresholds",
            skill_context=skill_context,
            content="Extended memory utilization is 97%.",
        )

        self.assertNotIn("Extended memory utilization | < 80%", planner_prompt)
        self.assertIn("reference_ids", planner_prompt)
        self.assertIn("Extended memory utilization", domain_prompt)


if __name__ == "__main__":
    unittest.main()
