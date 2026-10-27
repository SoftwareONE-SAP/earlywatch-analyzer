"""Decision-1 client: switched off by default, never raises, no real network."""
from __future__ import annotations

import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ewa_pipeline.agents.decision_client import decide
from ewa_pipeline.config import Config, _runtime_env

OPTIONS = {"true": "same issue", "false": "different issue"}


def make_config(**extra) -> Config:
    return Config.model_validate({
        "azure_openai": {
            "endpoint": "https://example.openai.azure.com/openai/v1",
            "api_key": "dummy",
            "api_version": "2025-03-01-preview",
            "deployments": {"orchestrator": "o", "specialist": "s"},
        },
        "reasoning": {"orchestrator": "low", "deep": "low"},
        **extra,
    })


class FakeResponse:
    def __init__(self, status=200, payload=None, bad_json=False):
        self.status_code = status
        self._payload = payload
        self._bad_json = bad_json

    def json(self):
        if self._bad_json:
            raise ValueError("bad json")
        return self._payload


class FakePost:
    def __init__(self, response=None, error=None):
        self.response, self.error, self.calls = response, error, []

    def __call__(self, url, **kwargs):
        self.calls.append((url, kwargs))
        if self.error:
            raise self.error
        return self.response


def ok(value):
    return FakeResponse(payload={"answers": {"answer": {"noul": value}}})


class DecisionClientTests(unittest.TestCase):
    def setUp(self):
        self.config = make_config(decision_enabled=True)

    def run_decide(self, post, config=None):
        return decide("Same?", OPTIONS, "ctx", config=config or self.config, post=post)

    def test_disabled_makes_no_call(self):
        post = FakePost(ok(0.9))
        self.assertEqual(self.run_decide(post, make_config()), {})
        self.assertEqual(post.calls, [])

    def test_success_request_and_result(self):
        post = FakePost(ok(0.75))
        result = decide("Same?", OPTIONS, {"a": 1}, config=self.config, post=post)
        self.assertEqual(result, {"true": 0.75, "false": 0.25})
        url, kwargs = post.calls[0]
        self.assertEqual(url, "https://example.openai.azure.com/providers/microsoft/v1/systemone")
        self.assertEqual(kwargs["headers"]["api-key"], "dummy")
        self.assertEqual(kwargs["json"], {
            "model": "Decision-1",
            "state": {"a": 1},
            "questions": {"answer": {"type": "noul", "instructions": "Same?", "criteria": OPTIONS}},
        })

    def test_http_error_status(self):
        self.assertEqual(self.run_decide(FakePost(FakeResponse(status=500))), {})

    def test_post_raises(self):
        self.assertEqual(self.run_decide(FakePost(error=OSError("down"))), {})

    def test_bad_json_and_missing_noul(self):
        self.assertEqual(self.run_decide(FakePost(FakeResponse(bad_json=True))), {})
        self.assertEqual(self.run_decide(FakePost(FakeResponse(payload={"answers": {}}))), {})
        self.assertEqual(self.run_decide(FakePost(ok("high"))), {})

    def test_out_of_range(self):
        self.assertEqual(self.run_decide(FakePost(ok(1.5))), {})
        self.assertEqual(self.run_decide(FakePost(ok(-0.1))), {})

    def test_env_settings(self):
        with patch.dict(os.environ, {"DECISION_ENABLED": "true", "DECISION_MODEL": "Decision-2"}):
            config = make_config(**_runtime_env())
        self.assertTrue(config.decision_enabled)
        self.assertEqual(config.decision_model, "Decision-2")
        self.assertFalse(make_config().decision_enabled)


if __name__ == "__main__":
    unittest.main()
