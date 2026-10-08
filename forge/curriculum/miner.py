from __future__ import annotations

from collections import defaultdict

from pydantic import BaseModel, Field

from forge.evaluation.schema import CaseResult


class FailureCluster(BaseModel):
    key: str
    count: int
    case_ids: list[str] = Field(default_factory=list)
    mean_score: float = 0.0


def cluster_failures(cases: list[CaseResult]) -> list[FailureCluster]:
    buckets: dict[str, list[CaseResult]] = defaultdict(list)
    for case in cases:
        if case.passed:
            continue
        keys = case.tags or ["unclassified"]
        for key in keys:
            buckets[key].append(case)
    clusters = []
    for key, rows in buckets.items():
        clusters.append(
            FailureCluster(
                key=key,
                count=len(rows),
                case_ids=[x.case_id for x in rows],
                mean_score=sum(x.score for x in rows) / len(rows),
            )
        )
    return sorted(clusters, key=lambda x: (x.count, -x.mean_score), reverse=True)
