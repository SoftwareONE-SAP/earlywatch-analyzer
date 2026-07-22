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

    def test_suggest_references_covers_new_specialist_domains(self) -> None:
        registry = self._registry()

        hana = registry.suggest_references(
            "ewa-analysis",
            "SAP HANA delta merge, service restarts, and backup recovery",
        )
        gateway = registry.suggest_references(
            "ewa-analysis",
            "SAP NetWeaver Gateway OData error log and metadata cache",
        )
        data_quality = registry.suggest_references(
            "ewa-analysis",
            "Service Data Quality is grey because SDCCN data is missing",
        )

        self.assertEqual("core-analysis", hana[0])
        self.assertIn("thresholds-hana", hana)
        self.assertIn("remediation-hana", hana)
        self.assertNotIn("thresholds-continuity", hana)
        self.assertNotIn("remediation-continuity", hana)
        hana_context = registry.resolve_context("ewa-analysis", hana)
        self.assertNotIn("Skill context truncated by backend limit", hana_context)
        self.assertIn("thresholds-integration", gateway)
        self.assertIn("remediation-integration", gateway)
        self.assertIn("thresholds-data-quality", data_quality)
        self.assertIn("remediation-data-quality", data_quality)

        hana_security = registry.suggest_references(
            "ewa-analysis",
            "SAP HANA Audit Trail and DATA ADMIN system privilege",
        )
        self.assertIn("thresholds-security", hana_security)
        self.assertIn("remediation-security", hana_security)
        self.assertNotIn("thresholds-hana", hana_security)
        self.assertNotIn("remediation-hana", hana_security)
        hana_security_context = registry.resolve_context("ewa-analysis", hana_security)
        self.assertNotIn("Skill context truncated by backend limit", hana_security_context)

        rfc_load = registry.suggest_references(
            "ewa-analysis",
            "RFC Load by Initiating Action",
        )
        self.assertIn("thresholds-integration", rfc_load)
        self.assertNotIn("thresholds-security", rfc_load)

    def test_typical_threshold_and_remediation_context_is_not_truncated(self) -> None:
        context = self._registry().resolve_context(
            "ewa-analysis",
            ["core-analysis", "thresholds-hana", "remediation-hana"],
        )

        self.assertIn("# Reference: core-analysis", context)
        self.assertIn("# Reference: remediation-hana", context)
        self.assertIn("# Reference: thresholds-hana", context)
        self.assertNotIn("Skill context truncated by backend limit", context)

    def test_new_reference_context_stays_lazy_and_domain_specific(self) -> None:
        context = self._registry().resolve_context(
            "ewa-analysis",
            ["thresholds-data-quality", "remediation-data-quality"],
        )

        self.assertIn("EWA Service Data Quality Assessment", context)
        self.assertIn("SDCCN", context)
        self.assertNotIn("Delta Merge", context)
        self.assertNotIn("Users with SAP_ALL in production", context)


if __name__ == "__main__":
    unittest.main()
