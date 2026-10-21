import importlib.util
from pathlib import Path
import unittest


GUARD_PATH = Path(__file__).resolve().parents[1] / "guard.py"
SPEC = importlib.util.spec_from_file_location("workshop_guard", GUARD_PATH)
GUARD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GUARD)


class GuardContractTests(unittest.TestCase):
    def assert_denied(self, payload):
        actual = GUARD.evaluate(payload)
        self.assertEqual(actual.get("permissionDecision"), "deny")
        self.assertTrue(actual.get("permissionDecisionReason"))

    def test_null_arguments_are_denied(self):
        self.assert_denied({"toolName": "bash", "toolArgs": None})

    def test_null_tool_name_is_denied(self):
        self.assert_denied({"toolName": None, "toolArgs": {"command": "ls"}})
        self.assert_denied({"tool_name": None, "tool_input": {"command": "ls"}})

    def test_list_arguments_are_denied(self):
        self.assert_denied({"toolName": "bash", "toolArgs": []})


if __name__ == "__main__":
    unittest.main()
