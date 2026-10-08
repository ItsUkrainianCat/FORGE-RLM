from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass


@dataclass
class TournamentResult:
    name: str
    score: float
    artifact: object
    notes: str = ""


def run_optimizer_tournament(
    optimizers: dict[str, Callable[[], tuple[float, object]]],
) -> list[TournamentResult]:
    """Run optimizer candidates behind a common interface.

    Use on development data only. Holdout evaluation belongs to the promotion gate.
    """
    results = []
    for name, fn in optimizers.items():
        score, artifact = fn()
        results.append(TournamentResult(name=name, score=score, artifact=artifact))
    return sorted(results, key=lambda x: x.score, reverse=True)
