import json
from pathlib import Path
import subprocess
import unittest


GUARD = Path(__file__).resolve().parents[1] / "guard.sh"


def decision(command):
    """Pass the command to guard.sh as JSON data; it is never executed."""
    payload = {"toolName": "bash", "toolArgs": {"command": command}}
    result = subprocess.run(
        [str(GUARD)], input=json.dumps(payload), text=True,
        capture_output=True, check=True, timeout=5,
    )
    return json.loads(result.stdout)


class GuardFlagTests(unittest.TestCase):
    def assert_denied(self, commands):
        for command in commands:
            with self.subTest(command=command):
                self.assertEqual(decision(command)["permissionDecision"], "deny")

    def test_recursive_rm_flag_variants_are_denied(self):
        self.assert_denied((
            "rm -rf example",
            "rm -fr example",
            "rm -r example",
            "rm -R example",
            "rm --recursive example",
            "/bin/rm -rf example",
            "/bin/rm --recursive example",
        ))

    def test_force_push_flag_variants_are_denied(self):
        self.assert_denied((
            "git push --force",
            "git push -f",
            "git push -f origin topic",
            "git push origin topic --force",
            "git push --force-with-lease",
        ))

    def test_harmless_commands_are_allowed(self):
        for command in ("git status", "git push", "git push origin topic"):
            with self.subTest(command=command):
                self.assertEqual(decision(command), {})


if __name__ == "__main__":
    unittest.main()
