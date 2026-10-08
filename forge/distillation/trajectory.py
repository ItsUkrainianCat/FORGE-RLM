from __future__ import annotations

from pydantic import BaseModel, Field


class TrajectoryRecord(BaseModel):
    id: str
    query: str
    answer: str
    score: float = Field(ge=0.0, le=1.0)
    trace: list[dict] = Field(default_factory=list)
    genome_fingerprint: str
    provenance: list[str] = Field(default_factory=list)
    latency_ms: float = 0.0
    tags: list[str] = Field(default_factory=list)
