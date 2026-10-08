from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from forge.aide.promotion import paired_bootstrap_delta_ci


@dataclass(frozen=True)
class SequentialDecision:
    decision: Literal["accept", "reject", "continue"]
    seeds_used: int
    delta: float
    ci_low: float
    ci_high: float
    rationale: str


def sequential_promotion_decision(
    candidate: list[float],
    baseline: list[float],
    *,
    min_seeds: int = 3,
    max_seeds: int = 10,
    min_delta: float = 0.0,
    confidence: float = 0.90,
) -> SequentialDecision:
    if len(candidate) != len(baseline):
        raise ValueError("candidate and baseline must have equal paired seed counts")
    n = len(candidate)
    if n < min_seeds:
        return SequentialDecision(
            "continue", n, 0.0, float("-inf"), float("inf"), "minimum seeds not reached"
        )
    delta, lo, hi = paired_bootstrap_delta_ci(candidate, baseline, confidence=confidence)
    if lo > min_delta:
        return SequentialDecision(
            "accept", n, delta, lo, hi, "lower confidence bound clears promotion threshold"
        )
    if hi <= min_delta:
        return SequentialDecision(
            "reject", n, delta, lo, hi, "upper confidence bound cannot clear promotion threshold"
        )
    if n >= max_seeds:
        return SequentialDecision(
            "reject", n, delta, lo, hi, "max seeds reached without decisive improvement"
        )
    return SequentialDecision("continue", n, delta, lo, hi, "evidence remains inconclusive")
