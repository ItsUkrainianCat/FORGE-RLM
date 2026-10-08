from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass
from pathlib import Path

_SAFE_ID = re.compile(r"^[A-Za-z0-9_.-]+$")


@dataclass(frozen=True)
class CandidateWorkspace:
    candidate_id: str
    path: Path
    base_ref: str


class GitWorktreeManager:
    """Creates disposable candidate worktrees without constructing shell strings."""

    def __init__(self, repo: str | Path = ".", root: str | Path = ".forge/worktrees") -> None:
        self.repo = Path(repo).resolve()
        self.root = (
            (self.repo / root).resolve() if not Path(root).is_absolute() else Path(root).resolve()
        )

    def create(self, candidate_id: str, *, base_ref: str = "HEAD") -> CandidateWorkspace:
        if not _SAFE_ID.match(candidate_id):
            raise ValueError("candidate_id contains unsafe characters")
        self.root.mkdir(parents=True, exist_ok=True)
        path = (self.root / candidate_id).resolve()
        if self.root not in path.parents:
            raise ValueError("candidate workspace escaped configured root")
        if path.exists():
            raise FileExistsError(path)
        subprocess.run(
            ["git", "-C", str(self.repo), "worktree", "add", "--detach", str(path), base_ref],
            check=True,
            capture_output=True,
            text=True,
        )
        return CandidateWorkspace(candidate_id=candidate_id, path=path, base_ref=base_ref)

    def remove(self, workspace: CandidateWorkspace, *, force: bool = True) -> None:
        args = ["git", "-C", str(self.repo), "worktree", "remove"]
        if force:
            args.append("--force")
        args.append(str(workspace.path))
        subprocess.run(args, check=True, capture_output=True, text=True)
