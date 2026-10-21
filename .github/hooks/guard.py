#!/usr/bin/env python3
"""Learning guardrail: inspect tool arguments without executing their content."""

import json
from pathlib import PurePosixPath
import shlex
import sys


def deny(reason):
    return {"permissionDecision": "deny", "permissionDecisionReason": reason}


def protected_path(value):
    name = PurePosixPath(value.replace("\\", "/").split("=", 1)[-1]).name
    return name != ".env.example" and (name == ".env" or name.startswith(".env."))


def evaluate(payload):
    if not isinstance(payload, dict):
        return deny("Guardrail input must be a JSON object.")
    tool = payload.get("toolName", payload.get("tool_name"))
    args = payload.get("toolArgs", payload.get("tool_input"))
    if isinstance(args, str):
        try:
            args = json.loads(args)
        except json.JSONDecodeError:
            return deny("Guardrail tool arguments must be valid JSON.")
    if not isinstance(tool, str) or not isinstance(args, dict):
        return deny("Guardrail requires a tool name and argument object.")

    for key in ("path", "file_path", "filePath", "filename"):
        value = args.get(key)
        if isinstance(value, str) and protected_path(value):
            return deny("Secret .env paths are blocked; use .env.example.")

    if tool.lower() not in {"bash", "shell", "execute", "powershell"}:
        return {}
    command = args.get("command")
    if not isinstance(command, str):
        return deny("Guardrail shell command must be a string.")
    try:
        tokens = shlex.split(command, posix=True)
    except ValueError:
        return deny("Guardrail could not parse the shell command.")

    if any(protected_path(token) for token in tokens):
        return deny("Secret .env paths are blocked; use .env.example.")
    for index, token in enumerate(tokens):
        name = PurePosixPath(token).name
        remaining = tokens[index + 1:]
        if name == "rm" and any(
            arg == "--recursive"
            or (arg.startswith("-") and not arg.startswith("--") and ("r" in arg or "R" in arg))
            for arg in remaining
        ):
            return deny("Recursive rm is blocked by the workshop guardrail.")
        if name == "git" and "push" in remaining:
            push_args = remaining[remaining.index("push") + 1:]
            if any(
                arg.startswith("--force")
                or (arg.startswith("-") and not arg.startswith("--") and "f" in arg)
                for arg in push_args
            ):
                return deny("Force push is blocked by the workshop guardrail.")
    return {}


def main():
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        decision = deny("Guardrail input is not valid JSON.")
    else:
        decision = evaluate(payload)
    print(json.dumps(decision))


if __name__ == "__main__":
    main()
