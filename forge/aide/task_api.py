from __future__ import annotations

from typing import Protocol

from forge.aide.schema import PublicEvaluation, ResearchBudget


class ResearchTask(Protocol):
    """Public side of an AI R&D optimization task."""

    task_id: str
    family: str
    budget: ResearchBudget

    def initial_artifact_ref(self) -> str: ...

    def evaluate_public(self, artifact_ref: str) -> PublicEvaluation: ...


class ResearchHarness(Protocol):
    """Candidate research agent/harness evaluated by the outer loop."""

    name: str

    def optimize(self, task: ResearchTask, *, seed: int) -> str:
        """Return the artifact selected by the harness under task.budget."""
        ...


class PrivateTaskScorer(Protocol):
    """Evaluator-only interface. Must not be given to the optimizing harness."""

    task_id: str

    def score_private(self, artifact_ref: str) -> float: ...
