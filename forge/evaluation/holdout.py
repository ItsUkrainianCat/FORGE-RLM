from __future__ import annotations

import os
from pathlib import Path


class HoldoutAccessError(PermissionError):
    pass


def holdout_path(filename: str = "cases.jsonl") -> Path:
    if os.getenv("FORGE_ALLOW_HOLDOUT", "false").lower() not in {"1", "true", "yes"}:
        raise HoldoutAccessError(
            "sealed holdout access disabled; evaluator must explicitly set FORGE_ALLOW_HOLDOUT=true"
        )
    base = Path(os.getenv("FORGE_HOLDOUT_DIR", ".forge/holdout"))
    path = base / filename
    if not path.exists():
        raise FileNotFoundError(path)
    return path
