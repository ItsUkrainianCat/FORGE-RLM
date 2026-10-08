from __future__ import annotations

from datetime import UTC, datetime
from typing import Literal

from pydantic import BaseModel, Field

MemoryCategory = Literal[
    "episodic", "semantic", "procedural", "experimental", "failure", "evidence", "decision"
]
MemoryStatus = Literal["hypothesis", "validated", "superseded", "failed", "retracted"]


class MemoryRecord(BaseModel):
    id: str
    category: MemoryCategory
    content: str
    source: str
    confidence: float = Field(ge=0.0, le=1.0)
    provenance: list[str] = Field(default_factory=list)
    status: MemoryStatus = "hypothesis"
    supersedes: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    outcome: str | None = None
    expires_at: datetime | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
