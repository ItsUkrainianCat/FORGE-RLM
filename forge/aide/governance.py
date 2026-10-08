from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from statistics import mean

from pydantic import BaseModel, Field


class AccelerationSnapshot(BaseModel):
    accepted_rewrites: int
    evaluated_candidates: int
    elapsed_hours: float
    incumbent_score: float
    baseline_score: float
    compute_cost_units: float
    autonomy_fraction: float = Field(ge=0.0, le=1.0)

    @property
    def acceptance_rate(self) -> float:
        return (
            self.accepted_rewrites / self.evaluated_candidates if self.evaluated_candidates else 0.0
        )

    @property
    def score_gain(self) -> float:
        return self.incumbent_score - self.baseline_score

    @property
    def gain_per_hour(self) -> float:
        return self.score_gain / self.elapsed_hours if self.elapsed_hours > 0 else 0.0

    @property
    def gain_per_cost(self) -> float:
        return self.score_gain / self.compute_cost_units if self.compute_cost_units > 0 else 0.0


@dataclass(frozen=True)
class ProgressionPolicy:
    """Conservative thresholds for pausing unexpectedly fast/opaque automation.

    These are operational guardrails, not claims that any threshold corresponds to
    an intelligence explosion. Configure from evidence and deployment context.
    """

    max_autonomy_fraction_without_review: float = 0.80
    max_accepted_rewrites_without_review: int = 10
    max_gain_per_hour_without_review: float = 0.05
    max_consecutive_outer_promotions: int = 3


class CapabilityAccelerationMonitor:
    def __init__(self, policy: ProgressionPolicy | None = None) -> None:
        self.policy = policy or ProgressionPolicy()
        self.history: list[AccelerationSnapshot] = []

    def observe(self, snapshot: AccelerationSnapshot) -> tuple[bool, list[str]]:
        self.history.append(snapshot)
        reasons: list[str] = []
        if snapshot.autonomy_fraction > self.policy.max_autonomy_fraction_without_review:
            reasons.append("autonomy fraction exceeds review threshold")
        if snapshot.accepted_rewrites > self.policy.max_accepted_rewrites_without_review:
            reasons.append("accepted rewrite count exceeds review threshold")
        if snapshot.gain_per_hour > self.policy.max_gain_per_hour_without_review:
            reasons.append("capability improvement velocity exceeds review threshold")
        return (not reasons, reasons)

    def recent_gain_velocity(self, n: int = 3) -> float:
        values = [s.gain_per_hour for s in self.history[-n:]]
        return mean(values) if values else 0.0


class PauseController:
    def __init__(self, sentinel: str | Path = ".forge/PAUSED") -> None:
        self.path = Path(sentinel)

    def is_paused(self) -> bool:
        return self.path.exists()

    def pause(self, reason: str) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(reason.strip() + "\n")

    def reason(self) -> str | None:
        return self.path.read_text().strip() if self.path.exists() else None

    def clear_with_explicit_approval(self, approval_token: str) -> None:
        # Deliberately simple local guard: caller must supply a non-empty explicit approval.
        # Production deployments should replace this with authenticated human approval.
        if len(approval_token.strip()) < 8:
            raise PermissionError("explicit human approval token required")
        self.path.unlink(missing_ok=True)
