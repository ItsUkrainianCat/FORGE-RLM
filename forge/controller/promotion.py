from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PromotionPolicy:
    min_dev_delta: float = 0.01
    max_latency_ratio: float = 2.0
    require_holdout: bool = True


def qualifies_for_holdout(
    *, dev_delta: float, critical_regressions: int, provenance_violations: int
) -> tuple[bool, str]:
    if critical_regressions:
        return False, "critical regression"
    if provenance_violations:
        return False, "provenance violation"
    if dev_delta <= 0:
        return False, "no dev improvement"
    return True, "qualified"


def promote_candidate(
    *,
    policy: PromotionPolicy,
    dev_delta: float,
    holdout_delta: float | None,
    latency_ratio: float,
    critical_regressions: int,
    catastrophic_failures: int,
) -> tuple[bool, str]:
    if critical_regressions or catastrophic_failures:
        return False, "critical/catastrophic regression"
    if dev_delta < policy.min_dev_delta:
        return False, "dev delta below threshold"
    if latency_ratio > policy.max_latency_ratio:
        return False, "latency regression exceeds policy"
    if policy.require_holdout and holdout_delta is None:
        return False, "holdout confirmation required"
    if holdout_delta is not None and holdout_delta <= 0:
        return False, "holdout did not improve"
    return True, "promotion criteria satisfied"
