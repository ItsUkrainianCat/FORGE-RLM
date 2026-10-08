from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Literal

import dspy


@dataclass(frozen=True)
class GepaPlan:
    auto: Literal["light", "medium", "heavy"] | None = "medium"
    max_full_evals: int | None = None
    max_metric_calls: int | None = None
    reflection_minibatch_size: int = 3
    candidate_selection_strategy: Literal["pareto", "current_best"] = "pareto"
    skip_perfect_score: bool = True
    add_format_failure_as_feedback: bool = True
    use_merge: bool = True
    max_merge_invocations: int | None = 5
    num_threads: int | None = None
    track_stats: bool = True
    track_best_outputs: bool = True
    use_mlflow: bool = False
    seed: int = 0
    log_dir: str | None = "artifacts/gepa"


_DEFAULT_GEPA_PLAN = GepaPlan()


def build_gepa(
    metric: Callable[..., Any],
    *,
    reflection_lm: dspy.LM | None = None,
    plan: GepaPlan = _DEFAULT_GEPA_PLAN,
    component_selector: str = "round_robin",
):
    """Centralize version-sensitive GEPA construction.

    Verify the installed DSPy API during environment audit; GEPA evolves rapidly.
    """
    if not hasattr(dspy, "GEPA"):
        raise RuntimeError("Installed DSPy does not expose dspy.GEPA")
    return dspy.GEPA(
        metric=metric,
        auto=plan.auto,
        max_full_evals=plan.max_full_evals,
        max_metric_calls=plan.max_metric_calls,
        reflection_minibatch_size=plan.reflection_minibatch_size,
        candidate_selection_strategy=plan.candidate_selection_strategy,
        reflection_lm=reflection_lm,
        skip_perfect_score=plan.skip_perfect_score,
        add_format_failure_as_feedback=plan.add_format_failure_as_feedback,
        component_selector=component_selector,
        use_merge=plan.use_merge,
        max_merge_invocations=plan.max_merge_invocations,
        num_threads=plan.num_threads,
        log_dir=plan.log_dir,
        track_stats=plan.track_stats,
        track_best_outputs=plan.track_best_outputs,
        use_mlflow=plan.use_mlflow,
        seed=plan.seed,
    )
