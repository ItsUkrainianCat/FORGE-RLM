from __future__ import annotations

import importlib.metadata as md
import os
import platform
import shutil
import subprocess


def version(cmd: list[str]) -> str:
    try:
        return (
            subprocess.check_output(cmd, text=True, stderr=subprocess.STDOUT, timeout=5)
            .strip()
            .splitlines()[0]
        )
    except Exception as exc:
        return f"unavailable ({exc.__class__.__name__})"


print("FORGE environment doctor")
print("OS:", platform.platform())
print("Python:", platform.python_version())
for pkg in ("dspy", "pydantic", "httpx"):
    try:
        print(f"{pkg}:", md.version(pkg))
    except md.PackageNotFoundError:
        print(f"{pkg}: NOT INSTALLED")
for name, cmd in {
    "git": ["git", "--version"],
    "node": ["node", "--version"],
    "npm": ["npm", "--version"],
    "deno": ["deno", "--version"],
    "claude": ["claude", "--version"],
    "ruflo": ["npx", "ruflo@latest", "--version"],
}.items():
    print(f"{name}:", version(cmd) if shutil.which(cmd[0]) else "NOT FOUND")
print("FORGE_API_BASE:", os.getenv("FORGE_API_BASE", "not set"))
