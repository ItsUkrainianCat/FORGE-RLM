from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, TypeVar

from forge.aide.governance import (
    AccelerationSnapshot,
    CapabilityAccelerationMonitor,
    PauseController,
)
from forge.aide.outer_loop import OuterLoopImprover, OuterLoopResult

CandidateT = TypeVar("CandidateT")


@dataclass
class AIDERunResult(Generic[CandidateT]):
    result: OuterLoopResult[CandidateT]
    paused: bool
    pause_reasons: list[str]


class AIDEEngine(Generic[CandidateT]):
    """Governed recursive AI R&D loop.

    The engine never receives sealed evaluation examples. It only receives grades
    through the outer-loop EvaluationAuthority. It can be paused independently of
    the model and cannot grant itself new permissions.
    """

    def __init__(
        self,
        *,
        outer_loop: OuterLoopImprover[CandidateT],
        monitor: CapabilityAccelerationMonitor | None = None,
        pause: PauseController | None = None,
    ) -> None:
        self.outer_loop = outer_loop
        self.monitor = monitor or CapabilityAccelerationMonitor()
        self.pause = pause or PauseController()

    def run(self, **outer_kwargs) -> AIDERunResult[CandidateT]:
        if self.pause.is_paused():
            raise RuntimeError(f"AIDE is paused: {self.pause.reason()}")
        result = self.outer_loop.run(**outer_kwargs)
        baseline = (
            result.records[0].incumbent_before
            if result.records
            else result.incumbent_grade.aggregate
        )
        total_cost = (
            sum(r.grade.compute_cost_units for r in result.records)
            or result.incumbent_grade.compute_cost_units
        )
        snapshot = AccelerationSnapshot(
            accepted_rewrites=result.accepted_rewrites,
            evaluated_candidates=len(result.records),
            elapsed_hours=max(1e-9, len(result.records) / 60.0),
            incumbent_score=result.incumbent_grade.aggregate,
            baseline_score=baseline,
            compute_cost_units=max(total_cost, 1e-9),
            autonomy_fraction=1.0,
        )
        allowed, reasons = self.monitor.observe(snapshot)
        if not allowed:
            self.pause.pause("; ".join(reasons))
        return AIDERunResult(result=result, paused=not allowed, pause_reasons=reasons)
