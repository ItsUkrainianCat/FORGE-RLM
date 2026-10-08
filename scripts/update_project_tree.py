from __future__ import annotations

from pathlib import Path

SKIP = {".git", ".venv", "__pycache__", ".pytest_cache", ".ruff_cache", ".mypy_cache"}


def main() -> None:
    root = Path(".")
    files = []
    for path in root.rglob("*"):
        if not path.is_file() or any(part in SKIP for part in path.parts):
            continue
        files.append(str(path).removeprefix("./"))
    Path("PROJECT_TREE.txt").write_text("\n".join(sorted(files)) + "\n")


if __name__ == "__main__":
    main()
