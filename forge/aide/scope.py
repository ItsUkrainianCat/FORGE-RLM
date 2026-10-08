from __future__ import annotations

from dataclasses import dataclass
from pathlib import PurePosixPath

from forge.aide.schema import PatchManifest


@dataclass(frozen=True)
class ScopePolicy:
    """Limits what an autonomous outer loop may propose changing.

    Evaluator authority, sealed holdouts, permission systems, and governance code are
    intentionally outside the autonomous mutation surface.
    """

    allowed_prefixes: tuple[str, ...] = (
        "forge/cognition/",
        "forge/rlm/",
        "forge/routing/",
        "forge/verification/",
        "forge/curriculum/",
        "forge/memory/",
        "forge/tools/",
        "prompts/",
        "config/",
    )
    forbidden_prefixes: tuple[str, ...] = (
        "evals/holdout/",
        ".forge/holdout/",
        "forge/evaluation/holdout.py",
        "forge/aide/governance.py",
        "forge/aide/scope.py",
        "forge/aide/private_grader.py",
        "docs/SOTA_GATE.md",
        "docs/SECURITY_BOUNDARIES.md",
        ".claude/settings.json",
        ".claude/hooks/",
    )

    def validate_path(self, raw: str) -> tuple[bool, str]:
        path = str(PurePosixPath(raw.replace("\\", "/")))
        if path.startswith("../") or path == ".." or path.startswith("/"):
            return False, "path escapes repository"
        if any(path == p or path.startswith(p) for p in self.forbidden_prefixes):
            return False, f"protected path: {path}"
        if not any(path.startswith(prefix) for prefix in self.allowed_prefixes):
            return False, f"outside autonomous mutation surface: {path}"
        return True, "allowed"

    def validate_manifest(self, manifest: PatchManifest) -> tuple[bool, list[str]]:
        problems: list[str] = []
        for op in manifest.operations:
            ok, reason = self.validate_path(op.path)
            if not ok:
                problems.append(f"{op.path}: {reason}")
        return (not problems, problems)
