from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DiverseCandidate:
    candidate_id: str
    score: float
    descriptor: tuple[str, ...]


class DiversityArchive:
    """Tiny quality-diversity archive: retain the best candidate per descriptor niche."""

    def __init__(self) -> None:
        self._niches: dict[tuple[str, ...], DiverseCandidate] = {}

    def add(self, candidate: DiverseCandidate) -> bool:
        current = self._niches.get(candidate.descriptor)
        if current is None or candidate.score > current.score:
            self._niches[candidate.descriptor] = candidate
            return True
        return False

    def candidates(self) -> list[DiverseCandidate]:
        return sorted(self._niches.values(), key=lambda c: c.score, reverse=True)

    def coverage(self) -> int:
        return len(self._niches)
