from __future__ import annotations

from datetime import UTC, datetime
from enum import Enum
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class StrategyArm(str, Enum):
    CONSERVATIVE = "conservative"
    AGGRESSIVE_REWRITE = "aggressive_rewrite"
    ENSEMBLE = "ensemble"
    TUNED_SPECIALIST = "tuned_specialist"
    ROBUST_SIMPLE = "robust_simple"


class OperatorKind(str, Enum):
    DRAFT = "draft"
    DEBUG = "debug"
    IMPROVE = "improve"
    SIMPLIFY = "simplify"
    AUDIT = "audit"


class CandidateStatus(str, Enum):
    CREATED = "created"
    SCORED = "scored"
    BUGGY = "buggy"
    REJECTED = "rejected"
    SELECTED = "selected"


class ResearchBudget(BaseModel):
    model_config = ConfigDict(extra="forbid")

    max_steps: int = Field(default=60, ge=1)
    max_model_calls: int = Field(default=120, ge=1)
    max_cost_units: float = Field(default=100.0, gt=0)
    max_wall_time_s: float = Field(default=3600.0, gt=0)


class BudgetUsage(BaseModel):
    steps: int = 0
    model_calls: int = 0
    cost_units: float = 0.0
    wall_time_s: float = 0.0


class PublicEvaluation(BaseModel):
    """Feedback visible to the inner loop."""

    score: float
    feedback: str = ""
    buggy: bool = False
    error_signature: str | None = None
    metrics: dict[str, float] = Field(default_factory=dict)


class CandidateProposal(BaseModel):
    artifact_ref: str
    summary: str
    model_calls: int = Field(default=1, ge=0)
    cost_units: float = Field(default=1.0, ge=0)
    metadata: dict[str, Any] = Field(default_factory=dict)


class CandidateNode(BaseModel):
    model_config = ConfigDict(extra="forbid")

    node_id: str
    parent_id: str | None = None
    strategy: StrategyArm
    operator: OperatorKind
    artifact_ref: str
    summary: str = ""
    public_score: float | None = None
    public_feedback: str = ""
    buggy: bool = False
    error_signature: str | None = None
    status: CandidateStatus = CandidateStatus.CREATED
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    metadata: dict[str, Any] = Field(default_factory=dict)


class PatchOperation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    path: str
    operation: Literal["create", "modify", "delete"]
    rationale: str


class PatchManifest(BaseModel):
    """Description of a proposed self-modification before it is applied."""

    operations: list[PatchOperation] = Field(default_factory=list)


class GenomeMutationSpec(BaseModel):
    path: str
    value: Any
    rationale: str


class ImprovementProposal(BaseModel):
    proposal_id: str
    parent_genome: str
    mutation_label: str
    target_failure_cluster: str
    hypothesis: str
    expected_effect: str
    patch: PatchManifest
    genome_mutations: list[GenomeMutationSpec] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class PrivateGrade(BaseModel):
    """Selection signal owned by the evaluator authority, not the inner agent."""

    aggregate: float
    seed_scores: list[float] = Field(default_factory=list)
    task_scores: dict[str, float] = Field(default_factory=dict)
    catastrophic_failures: int = 0
    reward_hacking_rate: float | None = None
    provenance_violations: int = 0
    compute_cost_units: float = 0.0
    metadata: dict[str, Any] = Field(default_factory=dict)


class OuterLoopRecord(BaseModel):
    step: int
    proposal_id: str
    parent_genome: str
    candidate_genome: str
    accepted: bool
    incumbent_before: float
    candidate_grade: float
    incumbent_after: float
    rationale: str
    grade: PrivateGrade


class AIDEConfig(BaseModel):
    """Controls a recursive self-improvement run.

    Defaults mirror useful design motifs from AIDE-style search while remaining
    configurable and testable rather than hard-coded as doctrine.
    """

    model_config = ConfigDict(extra="forbid")

    strategy_arms: list[StrategyArm] = Field(default_factory=lambda: list(StrategyArm))
    softmax_exploration_probability: float = Field(default=0.30, ge=0.0, le=1.0)
    softmax_temperature: float = Field(default=0.5, gt=0.0)
    fork_every_steps: int = Field(default=5, ge=1)
    recent_context_nodes: int = Field(default=6, ge=1)
    failure_memory_bug_rate_threshold: float = Field(default=0.15, ge=0.0, le=1.0)
    failure_memory_max_signatures: int = Field(default=3, ge=0, le=50)
    min_candidate_chars: int = Field(default=40, ge=1)
    outer_steps: int = Field(default=25, ge=1)
    require_fixed_budget: bool = True
    minimum_seeds_for_promotion: int = Field(default=3, ge=1)
    promotion_confidence: float = Field(default=0.90, gt=0.5, lt=1.0)
    min_private_delta: float = Field(default=0.0)
    max_candidate_latency_ratio: float = Field(default=2.0, ge=1.0)
    require_reward_hacking_check: bool = True
    require_external_generalization: bool = True
    require_human_approval_for_ignition: bool = True

    @model_validator(mode="after")
    def validate_arms(self) -> AIDEConfig:
        if not self.strategy_arms:
            raise ValueError("at least one strategy arm is required")
        if len(set(self.strategy_arms)) != len(self.strategy_arms):
            raise ValueError("strategy arms must be unique")
        return self
