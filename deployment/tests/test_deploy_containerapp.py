"""Offline regression checks for the Actions deployment's model settings migration."""
import importlib.util
import json
import subprocess
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("deploy_containerapp", Path(__file__).resolve().parents[1] / "deploy_containerapp.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def settings(**values):
    return {"container": "ewa-analyzer", "models": [{"name": key, "value": value} for key, value in values.items()],
            "legacyNames": [key for key in values if key.startswith("V2_")]}


class ModelMigrationTests(unittest.TestCase):
    def test_hyphenated_xhigh_is_corrected_for_known_reasoning_settings(self):
        names = ("ORCHESTRATOR_REASONING_EFFORT", "SPECIALIST_REASONING_EFFORT",
                 "CROSS_REFERENCE_REASONING_EFFORT", "SYNTHESIS_REASONING_EFFORT",
                 "CHAT_REASONING_EFFORT", "DEEP_REASONING_EFFORT")
        for name in names:
            with self.subTest(name=name):
                data = settings(ORCHESTRATOR_MODEL="planner", SPECIALIST_MODEL="worker", CHAT_MODEL="chat",
                                **{name: " x-HiGh "})
                self.assertEqual(module.migration(data), ([f"{name}=xhigh"], []))

    def test_valid_reasoning_and_unrelated_settings_are_preserved(self):
        data = settings(ORCHESTRATOR_MODEL="planner", SPECIALIST_MODEL="worker", CHAT_MODEL="chat",
                        ORCHESTRATOR_REASONING_EFFORT="xhigh", SPECIALIST_REASONING_EFFORT="high",
                        CROSS_REFERENCE_REASONING_EFFORT="none", SYNTHESIS_REASONING_EFFORT="medium",
                        CHAT_REASONING_EFFORT="low", DEEP_REASONING_EFFORT="", OTHER_SETTING="x-high")
        self.assertEqual(module.migration(data), ([], []))

    def test_reasoning_secret_references_are_not_read_or_replaced(self):
        data = settings(ORCHESTRATOR_MODEL="planner", SPECIALIST_MODEL="worker", CHAT_MODEL="chat")
        data["models"].append({"name": "SPECIALIST_REASONING_EFFORT", "secretRef": "reasoning-setting"})
        self.assertEqual(module.migration(data), ([], []))

    def test_reasoning_correction_is_applied_with_image_and_is_idempotent(self):
        data = settings(ORCHESTRATOR_MODEL="planner", SPECIALIST_MODEL="worker", CHAT_MODEL="chat",
                        SPECIALIST_REASONING_EFFORT="x-high")
        with patch.object(module.subprocess, "run", side_effect=[SimpleNamespace(stdout=json.dumps(data)),
                                                               SimpleNamespace(returncode=0)]) as run:
            module.deploy("ewa-analyzer", "test-group", "registry/app:commit")
        show = run.call_args_list[0].args[0]
        self.assertIn("SPECIALIST_REASONING_EFFORT", show[show.index("--query") + 1])
        update = run.call_args_list[1].args[0]
        self.assertEqual(update[update.index("--set-env-vars") + 1], "SPECIALIST_REASONING_EFFORT=xhigh")
        self.assertEqual(update[update.index("--image") + 1], "registry/app:commit")
        data["models"][-1]["value"] = "xhigh"
        self.assertEqual(module.migration(data), ([], []))

    def test_legacy_only_configuration_preserves_effective_models(self):
        data = settings(V2_ORCHESTRATOR_MODEL="old-planner-and-chat", V2_SPECIALIST_MODEL="old-worker",
                        V2_ROUTER_MODEL="old-router", V2_DEEP_MODEL="unused-deep")
        additions, removals = module.migration(data)
        self.assertEqual(additions, ["ORCHESTRATOR_MODEL=old-planner-and-chat", "SPECIALIST_MODEL=old-worker",
                                     "CHAT_MODEL=old-planner-and-chat"])
        self.assertEqual(set(removals), set(data["legacyNames"]))

    def test_current_portal_analysis_selections_are_preserved(self):
        data = settings(ORCHESTRATOR_MODEL="chosen-planner", SPECIALIST_MODEL="chosen-worker",
                        V2_ORCHESTRATOR_MODEL="existing-chat", V2_SPECIALIST_MODEL="obsolete-worker")
        additions, removals = module.migration(data)
        self.assertEqual(additions, ["CHAT_MODEL=existing-chat"])
        self.assertEqual(len(removals), 2)

    def test_existing_portal_chat_selection_is_never_overwritten(self):
        data = settings(ORCHESTRATOR_MODEL="planner", SPECIALIST_MODEL="worker", CHAT_MODEL="chosen-chat",
                        V2_ORCHESTRATOR_MODEL="outdated-chat")
        additions, removals = module.migration(data)
        self.assertEqual(additions, [])
        self.assertEqual(removals, ["V2_ORCHESTRATOR_MODEL"])

    def test_rerun_after_cleanup_needs_no_settings_changes(self):
        data = settings(ORCHESTRATOR_MODEL="planner", SPECIALIST_MODEL="worker", CHAT_MODEL="chat")
        self.assertEqual(module.migration(data), ([], []))

    def test_missing_chat_model_fails_before_any_update(self):
        data = settings(ORCHESTRATOR_MODEL="planner", SPECIALIST_MODEL="worker")
        with patch.object(module.subprocess, "run", return_value=SimpleNamespace(stdout=json.dumps(data))) as run:
            with self.assertRaisesRegex(ValueError, "CHAT_MODEL"):
                module.deploy("ewa-analyzer", "test-group", "registry/app:test")
        run.assert_called_once()

    def test_secret_references_are_migrated_without_fetching_secret_values(self):
        data = settings(ORCHESTRATOR_MODEL="planner", SPECIALIST_MODEL="worker")
        data["models"].append({"name": "V2_ORCHESTRATOR_MODEL", "secretRef": "model-deployment"})
        data["legacyNames"] = ["V2_ORCHESTRATOR_MODEL"]
        self.assertEqual(module.migration(data)[0], ["CHAT_MODEL=secretref:model-deployment"])

    def test_image_and_scoped_settings_change_in_one_update(self):
        data = settings(ORCHESTRATOR_MODEL="planner", SPECIALIST_MODEL="worker", V2_ORCHESTRATOR_MODEL="chat",
                        V2_ROUTER_MODEL="router", V2_DEEP_MODEL="deep", V2_SPECIALIST_MODEL="obsolete")
        data["legacyNames"].append("UNRELATED_SETTING")
        with patch.object(module.subprocess, "run", side_effect=[SimpleNamespace(stdout=json.dumps(data)),
                                                               SimpleNamespace(returncode=0)]) as run:
            module.deploy("ewa-analyzer", "test-group", "registry/app:commit")
        self.assertEqual(run.call_count, 2)
        show = run.call_args_list[0].args[0]
        update = run.call_args_list[1].args[0]
        self.assertEqual(show[:3], ["az", "containerapp", "show"])
        self.assertNotIn("AZURE_OPENAI_API_KEY", show[show.index("--query") + 1])
        self.assertEqual(update[:3], ["az", "containerapp", "update"])
        self.assertEqual(update[update.index("--image") + 1], "registry/app:commit")
        self.assertEqual(update[update.index("--set-env-vars") + 1], "CHAT_MODEL=chat")
        self.assertIn("--remove-env-vars", update)
        self.assertNotIn("UNRELATED_SETTING", update)
        self.assertNotIn("--replace-env-vars", update)
        self.assertNotIn("--remove-all-env-vars", update)

    def test_failed_azure_read_cannot_trigger_a_partial_update(self):
        with patch.object(module.subprocess, "run", side_effect=subprocess.CalledProcessError(1, "az")) as run:
            with self.assertRaises(subprocess.CalledProcessError):
                module.deploy("ewa-analyzer", "test-group", "registry/app:test")
        run.assert_called_once()


if __name__ == "__main__":
    unittest.main()
