from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class VerificationResult:
    passed: bool
    stage: str
    feedback: str = ""
    score: float = 1.0


class VerificationStage(Protocol):
    name: str

    def verify(self, *, query: str, answer: str, evidence: str = "") -> VerificationResult: ...


class VerifierPipeline:
    def __init__(self, stages: list[VerificationStage]) -> None:
        self.stages = stages

    def verify(self, *, query: str, answer: str, evidence: str = "") -> list[VerificationResult]:
        results: list[VerificationResult] = []
        for stage in self.stages:
            result = stage.verify(query=query, answer=answer, evidence=evidence)
            results.append(result)
            if not result.passed:
                break
        return results
