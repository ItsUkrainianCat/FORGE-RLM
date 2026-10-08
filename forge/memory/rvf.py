from __future__ import annotations

from pathlib import Path


class RVFManager:
    """Portable-memory boundary. Never fabricate an RVF file by writing arbitrary text."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)

    def exists(self) -> bool:
        return self.path.exists()

    def require_valid_artifact(self) -> Path:
        if not self.path.exists():
            raise FileNotFoundError(
                f"RVF not initialized: {self.path}. Use the installed Ruflo/RuVector RVF tooling and document the command."
            )
        if self.path.stat().st_size == 0:
            raise ValueError(f"empty RVF artifact: {self.path}")
        return self.path
