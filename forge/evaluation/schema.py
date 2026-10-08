from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class EvalCase(BaseModel):
    id: str
    query: str
    context: str = ""
    grader: str = "exact_match"
    expected: Any = None
    tags: list[str] = Field(default_factory=list)
    critical: bool = False
    metadata: dict[str, Any] = Field(default_factory=dict)


class GraderResult(BaseModel):
    score: float = Field(ge=0.0, le=1.0)
    passed: bool
    feedback: str = ""
    metadata: dict[str, Any] = Field(default_factory=dict)


class CaseResult(BaseModel):
    case_id: str
    score: float
    passed: bool
    prediction: str
    expected: Any = None
    grader: str
    feedback: str = ""
    latency_ms: float = 0.0
    route: str | None = None
    critical: bool = False
    tags: list[str] = Field(default_factory=list)
    trace_id: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
