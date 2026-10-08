from __future__ import annotations

from pydantic import BaseModel, Field


class PredictionEnvelope(BaseModel):
    answer: str
    route: str
    confidence: str = "unknown"
    latency_ms: float = Field(default=0.0, ge=0.0)
    trace_id: str | None = None
    evidence: list[str] = Field(default_factory=list)
    uncertainties: list[str] = Field(default_factory=list)
    metadata: dict = Field(default_factory=dict)
