from __future__ import annotations

from datetime import UTC, datetime
from typing import Literal

from pydantic import BaseModel, Field

from forge.genome.mutation import Mutation


class ExperimentPlan(BaseModel):
    experiment_id: str
    parent_genome: str
    target_failure_cluster: str
    hypothesis: str
    mutations: list[Mutation]
    expected_effect: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class ExperimentDecision(BaseModel):
    experiment_id: str
    decision: Literal["promote", "reject", "hold", "invalid"]
    rationale: str
    candidate_genome: str | None = None
