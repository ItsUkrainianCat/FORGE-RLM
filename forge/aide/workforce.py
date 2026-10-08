from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ResearchJob:
    job_id: str
    expected_value: float
    compute_cost: float
    duplicate_risk: float = 0.0
    hard_to_automate: float = 0.0
    wall_time_hours: float = 0.0


@dataclass(frozen=True)
class Allocation:
    job_id: str
    priority: float


class ResearchWorkforceScheduler:
    """Budget-aware R&D allocation with explicit diminishing-return/friction terms."""

    def rank(self, jobs: list[ResearchJob]) -> list[Allocation]:
        allocations = []
        for job in jobs:
            denominator = max(job.compute_cost, 1e-9)
            friction = (
                1.0
                + job.duplicate_risk
                + job.hard_to_automate
                + min(job.wall_time_hours / 24.0, 5.0)
            )
            priority = job.expected_value / denominator / friction
            allocations.append(Allocation(job_id=job.job_id, priority=priority))
        return sorted(allocations, key=lambda x: x.priority, reverse=True)
