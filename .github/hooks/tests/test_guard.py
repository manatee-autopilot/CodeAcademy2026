import json
from pathlib import Path
import subprocess
import unittest


GUARD = Path(__file__).resolve().parents[1] / "guard.sh"


def decision(payload):
    result = subprocess.run(
        [str(GUARD)], input=json.dumps(payload), text=True,
        capture_output=True, check=True, timeout=5,
    )
    return json.loads(result.stdout)


class GuardTests(unittest.TestCase):
    def test_recursive_remove_is_denied_without_execution(self):
        for command in ("rm -rf example", "rm -fr example", "/bin/rm --recursive example"):
            with self.subTest(command=command):
                actual = decision({"toolName": "bash", "toolArgs": {"command": command}})
                self.assertEqual(actual["permissionDecision"], "deny")

    def test_force_push_is_denied_without_execution(self):
        for command in ("git push --force", "git push -f origin topic", "git push --force-with-lease"):
            with self.subTest(command=command):
                actual = decision({"toolName": "bash", "toolArgs": {"command": command}})
                self.assertEqual(actual["permissionDecision"], "deny")

    def test_secret_paths_are_denied_without_reading(self):
        payloads = [
            {"toolName": "bash", "toolArgs": {"command": "cat .env"}},
            {"toolName": "view", "toolArgs": {"path": "/project/.env.local"}},
            {"tool_name": "Read", "tool_input": {"file_path": ".env"}},
        ]
        for payload in payloads:
            with self.subTest(payload=payload):
                self.assertEqual(decision(payload)["permissionDecision"], "deny")

    def test_safe_calls_defer_to_normal_permissions(self):
        for payload in (
            {"toolName": "bash", "toolArgs": {"command": "git status --short"}},
            {"toolName": "bash", "toolArgs": {"command": "cat .env.example"}},
            {"toolName": "view", "toolArgs": {"path": "README.md"}},
            {"toolName": "edit", "toolArgs": {"path": "guard.py", "new_str": "Document .env handling"}},
        ):
            with self.subTest(payload=payload):
                self.assertEqual(decision(payload), {})

    def test_serialized_arguments_are_supported(self):
        self.assertEqual(
            decision({"toolName": "bash", "toolArgs": json.dumps({"command": "git status"})}),
            {},
        )

    def test_malformed_inputs_are_denied(self):
        for payload in ([], {}, {"toolName": "bash", "toolArgs": "not JSON"},
                        {"toolName": "bash", "toolArgs": {"command": "'"}}):
            with self.subTest(payload=payload):
                self.assertEqual(decision(payload)["permissionDecision"], "deny")

    def test_invalid_json_is_denied(self):
        result = subprocess.run(
            [str(GUARD)], input="{", text=True, capture_output=True,
            check=True, timeout=5,
        )
        self.assertEqual(json.loads(result.stdout)["permissionDecision"], "deny")


if __name__ == "__main__":
    unittest.main()
