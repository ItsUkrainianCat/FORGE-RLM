from forge.aide.benchmark import BenchmarkItem, HarnessBenchmark
from forge.aide.schema import PublicEvaluation, ResearchBudget


class Task:
    task_id = "t"
    family = "toy"
    budget = ResearchBudget(max_steps=1, max_model_calls=1, max_cost_units=2, max_wall_time_s=10)

    def initial_artifact_ref(self):
        return "root"

    def evaluate_public(self, artifact_ref):
        return PublicEvaluation(score=0.0)


class Scorer:
    task_id = "t"

    def score_private(self, artifact_ref):
        return float(artifact_ref.split(":")[-1])


class Harness:
    name = "h"

    def optimize(self, task, *, seed):
        return f"artifact:{0.7 + seed * 0.001}"


def test_harness_benchmark_uses_private_task_scores_across_seeds():
    b = HarnessBenchmark([BenchmarkItem(Task(), Scorer())], seeds=[1, 2, 3])
    grade = b.grade(Harness())
    assert len(grade.seed_scores) == 3
    assert grade.aggregate > 0.70
    assert grade.compute_cost_units == 2
