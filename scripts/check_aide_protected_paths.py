from __future__ import annotations

import subprocess
from pathlib import Path

from forge.aide.scope import ScopePolicy


def changed_files() -> list[str]:
    commands = [
        ["git", "diff", "--name-only"],
        ["git", "diff", "--cached", "--name-only"],
    ]
    names: set[str] = set()
    for cmd in commands:
        try:
            out = subprocess.check_output(cmd, text=True, stderr=subprocess.DEVNULL)
        except (subprocess.CalledProcessError, FileNotFoundError):
            continue
        names.update(line.strip() for line in out.splitlines() if line.strip())
    return sorted(names)


def main() -> int:
    if not Path(".forge/AIDE_AUTONOMOUS").exists():
        return 0
    policy = ScopePolicy()
    problems: list[str] = []
    for path in changed_files():
        # Existing harness changes may be legal. Only protected/out-of-scope autonomous diffs fail.
        ok, reason = policy.validate_path(path)
        if not ok:
            problems.append(f"{path}: {reason}")
    if problems:
        print("AIDE autonomous mutation boundary violation:")
        for problem in problems:
            print(f"- {problem}")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
