from __future__ import annotations

import json
import re
from collections.abc import Callable
from typing import Any

from forge.evaluation.schema import EvalCase, GraderResult

Grader = Callable[[EvalCase, str], GraderResult]


def _norm(value: Any) -> str:
    return " ".join(str(value).strip().lower().split())


def exact_match(case: EvalCase, prediction: str) -> GraderResult:
    passed = _norm(prediction) == _norm(case.expected)
    return GraderResult(
        score=float(passed), passed=passed, feedback="exact match" if passed else "exact mismatch"
    )


def contains(case: EvalCase, prediction: str) -> GraderResult:
    expected = case.expected if isinstance(case.expected, list) else [case.expected]
    missing = [str(x) for x in expected if _norm(x) not in _norm(prediction)]
    passed = not missing
    return GraderResult(
        score=1.0 if passed else max(0.0, 1.0 - len(missing) / max(len(expected), 1)),
        passed=passed,
        feedback=f"missing: {missing}" if missing else "all required content present",
    )


def regex(case: EvalCase, prediction: str) -> GraderResult:
    patterns = case.expected if isinstance(case.expected, list) else [case.expected]
    missing = [
        str(p)
        for p in patterns
        if not re.search(str(p), prediction, flags=re.IGNORECASE | re.MULTILINE)
    ]
    passed = not missing
    return GraderResult(
        score=1.0 if passed else 0.0,
        passed=passed,
        feedback=f"unmatched patterns: {missing}" if missing else "patterns matched",
    )


def json_valid(case: EvalCase, prediction: str) -> GraderResult:
    try:
        parsed = json.loads(prediction)
    except json.JSONDecodeError as exc:
        return GraderResult(score=0.0, passed=False, feedback=f"invalid JSON: {exc}")
    if case.expected is None:
        return GraderResult(score=1.0, passed=True, feedback="valid JSON")
    expected_keys = set(case.expected if isinstance(case.expected, list) else [case.expected])
    if not isinstance(parsed, dict):
        return GraderResult(score=0.0, passed=False, feedback="expected JSON object")
    missing = sorted(expected_keys - set(parsed))
    return GraderResult(
        score=1.0 if not missing else 0.0,
        passed=not missing,
        feedback=f"missing keys: {missing}" if missing else "valid JSON object",
    )


DEFAULT_GRADERS: dict[str, Grader] = {
    "exact_match": exact_match,
    "contains": contains,
    "regex": regex,
    "json_valid": json_valid,
}
