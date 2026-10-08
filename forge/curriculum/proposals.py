from __future__ import annotations

from pydantic import BaseModel, Field


class TaskProposal(BaseModel):
    source_cluster: str
    objective: str
    prompt_template: str
    difficulty: float = Field(ge=0.0, le=1.0)
    validation_plan: str
    target_split: str = "train"


def boundary_variants(*, cluster: str, base_prompt: str) -> list[TaskProposal]:
    """Deterministic scaffolds only; a teacher/evaluator may later instantiate them."""
    return [
        TaskProposal(
            source_cluster=cluster,
            objective="near-boundary paraphrase",
            prompt_template=f"Rephrase while preserving the governing difficulty: {base_prompt}",
            difficulty=0.6,
            validation_plan="independent grader/teacher validation",
        ),
        TaskProposal(
            source_cluster=cluster,
            objective="adversarial distractor variant",
            prompt_template=f"Add irrelevant but plausible context without changing the correct solution: {base_prompt}",
            difficulty=0.75,
            validation_plan="independent grader/teacher validation",
        ),
    ]
