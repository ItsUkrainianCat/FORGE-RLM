from __future__ import annotations

import math
import random
from statistics import mean


def bootstrap_mean_ci(
    values: list[float], *, confidence: float = 0.95, samples: int = 2000, seed: int = 0
) -> tuple[float, float]:
    if not values:
        return (0.0, 0.0)
    if len(values) == 1:
        return (values[0], values[0])
    rng = random.Random(seed)
    n = len(values)
    boot = [mean(rng.choice(values) for _ in range(n)) for _ in range(samples)]
    boot.sort()
    alpha = (1.0 - confidence) / 2.0
    lo = boot[max(0, math.floor(alpha * samples))]
    hi = boot[min(samples - 1, math.ceil((1.0 - alpha) * samples) - 1)]
    return (lo, hi)


def paired_delta(candidate: list[float], baseline: list[float]) -> float:
    if len(candidate) != len(baseline):
        raise ValueError("paired samples must have the same length")
    if not candidate:
        return 0.0
    return mean(c - b for c, b in zip(candidate, baseline, strict=True))
