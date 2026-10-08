from __future__ import annotations

import time
from collections.abc import Callable
from pathlib import Path

from forge.evaluation.dataset import load_cases
from forge.evaluation.registry import GraderRegistry
from forge.evaluation.report import EvaluationReport, build_report
from forge.evaluation.schema import CaseResult
from forge.runtime.envelope import PredictionEnvelope

Predictor = Callable[[str, str], str | PredictionEnvelope]


class EvaluationRunner:
    def __init__(self, registry: GraderRegistry | None = None) -> None:
        self.registry = registry or GraderRegistry()

    def evaluate(
        self,
        *,
        path: Path,
        predictor: Predictor,
        split: str,
        limit: int | None = None,
        genome_fingerprint: str | None = None,
    ) -> EvaluationReport:
        cases = load_cases(path)
        if limit:
            cases = cases[:limit]
        results: list[CaseResult] = []
        for case in cases:
            start = time.perf_counter()
            raw = predictor(case.query, case.context)
            elapsed = (time.perf_counter() - start) * 1000
            if isinstance(raw, PredictionEnvelope):
                prediction = raw.answer
                latency = raw.latency_ms or elapsed
                route = raw.route
                trace_id = raw.trace_id
                metadata = raw.metadata
            else:
                prediction = str(raw)
                latency = elapsed
                route = None
                trace_id = None
                metadata = {}
            grader = self.registry.get(case.grader)
            grade = grader(case, prediction)
            results.append(
                CaseResult(
                    case_id=case.id,
                    score=grade.score,
                    passed=grade.passed,
                    prediction=prediction,
                    expected=case.expected,
                    grader=case.grader,
                    feedback=grade.feedback,
                    latency_ms=latency,
                    route=route,
                    critical=case.critical,
                    tags=case.tags,
                    trace_id=trace_id,
                    metadata={**metadata, **grade.metadata},
                )
            )
        return build_report(split, results, genome_fingerprint=genome_fingerprint)


def evaluate_jsonl(path: Path, predict: Callable[[str], str], limit: int | None = None) -> dict:
    """Backward-compatible wrapper around the v3 evaluator."""
    runner = EvaluationRunner()
    report = runner.evaluate(
        path=path, predictor=lambda q, _c: predict(q), split=path.parent.name, limit=limit
    )
    return report.model_dump(mode="json")
