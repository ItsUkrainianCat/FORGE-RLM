from __future__ import annotations

from collections.abc import Callable
from statistics import mean

from pydantic import BaseModel, Field


class IgnitionArmResult(BaseModel):
    name: str
    endpoints: list[float] = Field(default_factory=list)
    steps_to_threshold: list[int | None] = Field(default_factory=list)

    @property
    def mean_endpoint(self) -> float:
        return mean(self.endpoints) if self.endpoints else 0.0

    @property
    def mean_steps_to_threshold(self) -> float | None:
        vals = [x for x in self.steps_to_threshold if x is not None]
        return mean(vals) if vals else None


class IgnitionReport(BaseModel):
    treatment: IgnitionArmResult
    reference: IgnitionArmResult
    endpoint_delta: float
    faster_to_threshold: bool | None
    passed_non_degradation: bool
    promote_to_outer_loop: bool
    rationale: str


def run_ignition_test(
    *,
    treatment_name: str,
    reference_name: str,
    seeds: list[int],
    run_outer_loop: Callable[[str, int], tuple[float, int | None]],
    noninferiority_margin: float = 0.0,
    require_strict_improvement: bool = True,
) -> IgnitionReport:
    treatment_endpoints: list[float] = []
    reference_endpoints: list[float] = []
    treatment_steps: list[int | None] = []
    reference_steps: list[int | None] = []
    for seed in seeds:
        t_end, t_steps = run_outer_loop(treatment_name, seed)
        r_end, r_steps = run_outer_loop(reference_name, seed)
        treatment_endpoints.append(t_end)
        reference_endpoints.append(r_end)
        treatment_steps.append(t_steps)
        reference_steps.append(r_steps)

    t = IgnitionArmResult(
        name=treatment_name, endpoints=treatment_endpoints, steps_to_threshold=treatment_steps
    )
    r = IgnitionArmResult(
        name=reference_name, endpoints=reference_endpoints, steps_to_threshold=reference_steps
    )
    delta = t.mean_endpoint - r.mean_endpoint
    non_degrade = delta >= -noninferiority_margin
    faster: bool | None = None
    if t.mean_steps_to_threshold is not None and r.mean_steps_to_threshold is not None:
        faster = t.mean_steps_to_threshold < r.mean_steps_to_threshold
    if require_strict_improvement:
        promote = non_degrade and delta > 0 and (faster is not False)
    else:
        promote = non_degrade and (delta > 0 or faster is True)
    rationale = (
        f"endpoint delta={delta:.6f}; non-degradation={non_degrade}; "
        f"faster_to_threshold={faster}; strict={require_strict_improvement}"
    )
    return IgnitionReport(
        treatment=t,
        reference=r,
        endpoint_delta=delta,
        faster_to_threshold=faster,
        passed_non_degradation=non_degrade,
        promote_to_outer_loop=promote,
        rationale=rationale,
    )
