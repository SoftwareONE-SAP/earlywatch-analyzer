from __future__ import annotations

import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from core.runtime_config import get_reasoning_effort  # noqa: E402


class RuntimeConfigTests(unittest.TestCase):
    def test_reasoning_effort_is_read_from_environment(self) -> None:
        with patch.dict(os.environ, {"TEST_REASONING_EFFORT": " High "}):
            self.assertEqual("high", get_reasoning_effort("TEST_REASONING_EFFORT"))

    def test_reasoning_effort_is_required(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(RuntimeError, "TEST_REASONING_EFFORT"):
                get_reasoning_effort("TEST_REASONING_EFFORT")

    def test_reasoning_effort_rejects_unsupported_values(self) -> None:
        with patch.dict(os.environ, {"TEST_REASONING_EFFORT": "extreme"}):
            with self.assertRaisesRegex(RuntimeError, "must be one of"):
                get_reasoning_effort("TEST_REASONING_EFFORT")


if __name__ == "__main__":
    unittest.main()
