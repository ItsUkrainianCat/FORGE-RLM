from __future__ import annotations

from pydantic import BaseModel, Field


class CapabilityScore(BaseModel):
    name: str
    score: float = Field(ge=0.0, le=1.0)
    sample_count: int = Field(default=0, ge=0)
    failure_rate: float = Field(default=0.0, ge=0.0, le=1.0)
    impact: float = Field(default=1.0, ge=0.0)
    cost: float = Field(default=0.0, ge=0.0)


class CapabilityReport(BaseModel):
    genome_fingerprint: str
    capabilities: list[CapabilityScore]

    def bottlenecks(self, limit: int = 5) -> list[CapabilityScore]:
        def priority(x: CapabilityScore) -> float:
            return (1.0 - x.score) * x.impact + x.failure_rate * 0.5 - x.cost * 0.05

        return sorted(self.capabilities, key=priority, reverse=True)[:limit]

    def as_dict(self) -> dict[str, float]:
        return {c.name: c.score for c in self.capabilities}
