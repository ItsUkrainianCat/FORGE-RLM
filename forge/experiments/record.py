from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, Field


class ExperimentRecord(BaseModel):
    experiment_id: str
    parent_genome: str
    candidate_genome: str
    hypothesis: str
    mutation_summary: list[str] = Field(default_factory=list)
    target_failure_cluster: str | None = None
    dev_metrics: dict[str, float] = Field(default_factory=dict)
    holdout_metrics: dict[str, float] = Field(default_factory=dict)
    cost_metrics: dict[str, float] = Field(default_factory=dict)
    critical_regressions: list[str] = Field(default_factory=list)
    decision: Literal["promote", "reject", "hold", "invalid"] = "hold"
    lesson: str = ""
    metadata: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class ExperimentStore:
    def __init__(self, directory: str | Path = "experiments") -> None:
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)

    def save(self, record: ExperimentRecord) -> Path:
        path = self.directory / f"{record.experiment_id}.json"
        path.write_text(json.dumps(record.model_dump(mode="json"), indent=2, default=str) + "\n")
        return path
