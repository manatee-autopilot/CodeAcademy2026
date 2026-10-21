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


def shell(command):
    return {"toolName": "bash", "toolArgs": {"command": command}}


class GuardPathTests(unittest.TestCase):
    def assertDenied(self, payload):
        self.assertEqual(decision(payload)["permissionDecision"], "deny")

    def test_quoted_shell_env_references_are_denied(self):
        for command in ('cat ".env"', "cat '.env'", 'cat "config/.env"',
                        "cat './app/.env.local'", 'cat ".env.production"'):
            with self.subTest(command=command):
                self.assertDenied(shell(command))

    def test_nested_secret_file_paths_are_denied(self):
        for path in ("config/.env", "a/b/c/.env.production", "/project/app/.env.local",
                     "apps\\api\\.env"):
            with self.subTest(path=path):
                self.assertDenied({"toolName": "view", "toolArgs": {"path": path}})
                self.assertDenied(shell("cat " + json.dumps(path.replace("\\", "/"))))

    def test_env_example_is_allowed(self):
        for path in (".env.example", "config/.env.example", "/project/app/.env.example"):
            with self.subTest(path=path):
                self.assertEqual(decision({"toolName": "view", "toolArgs": {"path": path}}), {})
                self.assertEqual(decision(shell("cat '" + path + "'")), {})

    def test_env_local_is_denied(self):
        self.assertDenied({"toolName": "view", "toolArgs": {"path": ".env.local"}})
        self.assertDenied(shell("cat .env.local"))

    def test_camel_and_snake_case_file_arguments_are_denied(self):
        for key in ("filePath", "file_path", "path", "filename"):
            with self.subTest(key=key):
                self.assertDenied({"toolName": "view", "toolArgs": {key: "svc/.env"}})
                self.assertDenied({"tool_name": "Read", "tool_input": {key: "svc/.env.local"}})

    def test_camel_and_snake_case_example_files_are_allowed(self):
        for key in ("filePath", "file_path"):
            with self.subTest(key=key):
                self.assertEqual(
                    decision({"toolName": "view", "toolArgs": {key: "svc/.env.example"}}), {})
                self.assertEqual(
                    decision({"tool_name": "Read", "tool_input": {key: ".env.example"}}), {})


if __name__ == "__main__":
    unittest.main()
