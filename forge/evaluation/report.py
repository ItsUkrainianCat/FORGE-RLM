from __future__ import annotations

from collections import Counter, defaultdict
from statistics import mean

from pydantic import BaseModel, Field

from forge.evaluation.schema import CaseResult
from forge.evaluation.stats import bootstrap_mean_ci


class EvaluationReport(BaseModel):
    split: str
    genome_fingerprint: str | None = None
    count: int
    mean_score: float
    ci95_low: float
    ci95_high: float
    passed: int
    failed: int
    critical_failures: int
    latency_mean_ms: float
    scores_by_tag: dict[str, float] = Field(default_factory=dict)
    failure_tags: dict[str, int] = Field(default_factory=dict)
    cases: list[CaseResult] = Field(default_factory=list)


def build_report(
    split: str, cases: list[CaseResult], *, genome_fingerprint: str | None = None
) -> EvaluationReport:
    scores = [c.score for c in cases]
    lo, hi = bootstrap_mean_ci(scores)
    by_tag: dict[str, list[float]] = defaultdict(list)
    failures = Counter()
    for case in cases:
        for tag in case.tags:
            by_tag[tag].append(case.score)
            if not case.passed:
                failures[tag] += 1
    return EvaluationReport(
        split=split,
        genome_fingerprint=genome_fingerprint,
        count=len(cases),
        mean_score=mean(scores) if scores else 0.0,
        ci95_low=lo,
        ci95_high=hi,
        passed=sum(c.passed for c in cases),
        failed=sum(not c.passed for c in cases),
        critical_failures=sum(c.critical and not c.passed for c in cases),
        latency_mean_ms=mean([c.latency_ms for c in cases]) if cases else 0.0,
        scores_by_tag={k: mean(v) for k, v in by_tag.items()},
        failure_tags=dict(failures),
        cases=cases,
    )
