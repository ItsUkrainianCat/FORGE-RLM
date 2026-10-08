from __future__ import annotations

from dataclasses import dataclass
from statistics import mean

from forge.aide.schema import PrivateGrade
from forge.aide.task_api import PrivateTaskScorer, ResearchHarness, ResearchTask


@dataclass(frozen=True)
class BenchmarkItem:
    task: ResearchTask
    private_scorer: PrivateTaskScorer


class HarnessBenchmark:
    """Grades a research harness by downstream task optimization capability.

    The harness sees ResearchTask/public feedback. PrivateTaskScorer remains inside
    the evaluator authority.
    """

    def __init__(self, items: list[BenchmarkItem], *, seeds: list[int]) -> None:
        if not items:
            raise ValueError("benchmark requires at least one task")
        if not seeds:
            raise ValueError("benchmark requires at least one seed")
        self.items = items
        self.seeds = seeds

    def grade(self, harness: ResearchHarness) -> PrivateGrade:
        seed_scores: list[float] = []
        task_accumulator: dict[str, list[float]] = {item.task.task_id: [] for item in self.items}
        total_cost = 0.0
        catastrophic = 0
        for seed in self.seeds:
            scores: list[float] = []
            for item in self.items:
                try:
                    artifact = harness.optimize(item.task, seed=seed)
                    score = item.private_scorer.score_private(artifact)
                except Exception:
                    catastrophic += 1
                    score = float("-1e6")
                scores.append(score)
                task_accumulator[item.task.task_id].append(score)
                total_cost += item.task.budget.max_cost_units
            seed_scores.append(mean(scores))
        task_scores = {task: mean(values) for task, values in task_accumulator.items()}
        return PrivateGrade(
            aggregate=mean(seed_scores),
            seed_scores=seed_scores,
            task_scores=task_scores,
            catastrophic_failures=catastrophic,
            compute_cost_units=total_cost / len(self.seeds),
        )
