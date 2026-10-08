from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class ComputeProfile(StrEnum):
    FAST = "fast"
    BALANCED = "balanced"
    DEEP = "deep"
    FORENSIC = "forensic"


@dataclass(frozen=True)
class ComputeSignals:
    estimated_difficulty: float
    consequence_risk: float = 0.0
    context_pressure: float = 0.0
    ambiguity: float = 0.0


def choose_compute_profile(signals: ComputeSignals) -> ComputeProfile:
    score = (
        signals.estimated_difficulty * 0.55
        + signals.consequence_risk * 0.20
        + signals.context_pressure * 0.15
        + signals.ambiguity * 0.10
    )
    if score < 0.25:
        return ComputeProfile.FAST
    if score < 0.55:
        return ComputeProfile.BALANCED
    if score < 0.80:
        return ComputeProfile.DEEP
    return ComputeProfile.FORENSIC


def expected_value_of_extra_compute(
    *,
    expected_quality_gain: float,
    latency_penalty: float,
    token_penalty: float,
    lam: float = 0.15,
    mu: float = 0.10,
) -> float:
    return expected_quality_gain - lam * latency_penalty - mu * token_penalty
