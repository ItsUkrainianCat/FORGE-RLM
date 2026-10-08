from __future__ import annotations

import hashlib
import json

from pydantic import BaseModel, ConfigDict, Field


class ModelGene(BaseModel):
    model_config = ConfigDict(extra="forbid")
    model_id: str = "qwen-local"
    quantization: str = "unknown"
    context_length: int = Field(default=32768, gt=0)


class InferenceGene(BaseModel):
    model_config = ConfigDict(extra="forbid")
    temperature: float = Field(default=0.2, ge=0.0, le=2.0)
    top_p: float = Field(default=0.9, gt=0.0, le=1.0)
    max_tokens: int = Field(default=4096, gt=0)
    reasoning_mode: str = "adaptive"


class RouterGene(BaseModel):
    model_config = ConfigDict(extra="forbid")
    version: str = "heuristic-v2"
    direct_threshold: float = Field(default=0.25, ge=0.0, le=1.0)
    deep_threshold: float = Field(default=0.70, ge=0.0, le=1.0)


class RLMGene(BaseModel):
    model_config = ConfigDict(extra="forbid")
    enabled: bool = True
    max_iters: int = Field(default=10, ge=1, le=100)
    max_llm_calls: int = Field(default=24, ge=1, le=500)
    max_output_chars: int = Field(default=10000, ge=1000)


class VerificationGene(BaseModel):
    model_config = ConfigDict(extra="forbid")
    enabled: bool = True
    stages: list[str] = Field(default_factory=lambda: ["deterministic", "lm_critic"])
    max_revisions: int = Field(default=1, ge=0, le=5)


class MemoryGene(BaseModel):
    model_config = ConfigDict(extra="forbid")
    enabled: bool = False
    backend: str = "ruvector"
    retrieval_k: int = Field(default=8, ge=1, le=100)
    policy: str = "epistemic-v1"


class ToolGene(BaseModel):
    model_config = ConfigDict(extra="forbid")
    enabled: bool = True
    router: str = "hierarchical-v1"
    allowed_domains: list[str] = Field(default_factory=list)


class OptimizerGene(BaseModel):
    model_config = ConfigDict(extra="forbid")
    dspy_program: str = "baseline-v0"
    gepa_candidate: str | None = None


class PersonaGene(BaseModel):
    model_config = ConfigDict(extra="forbid")
    enabled: bool = False
    version: str | None = None


class AIDEGene(BaseModel):
    model_config = ConfigDict(extra="forbid")
    enabled: bool = True
    version: str = "aide-rsi-v1"
    outer_steps: int = Field(default=25, ge=1, le=1000)
    strategy_policy: str = "ucb1-softmax-fork"
    fixed_budget: bool = True
    sealed_private_grading: bool = True
    ignition_required: bool = True


class GovernanceGene(BaseModel):
    model_config = ConfigDict(extra="forbid")
    progression_gates: bool = True
    pause_sentinel: str = ".forge/PAUSED"
    autonomous_mutation_scope: str = "harness-only"
    human_approval_for_ignition: bool = True
    self_granted_permissions_forbidden: bool = True


class CognitiveGenome(BaseModel):
    """Complete reproducible configuration of one FORGE candidate."""

    model_config = ConfigDict(extra="forbid")
    name: str
    parent: str | None = None
    model: ModelGene = Field(default_factory=ModelGene)
    inference: InferenceGene = Field(default_factory=InferenceGene)
    router: RouterGene = Field(default_factory=RouterGene)
    rlm: RLMGene = Field(default_factory=RLMGene)
    verification: VerificationGene = Field(default_factory=VerificationGene)
    memory: MemoryGene = Field(default_factory=MemoryGene)
    tools: ToolGene = Field(default_factory=ToolGene)
    optimizer: OptimizerGene = Field(default_factory=OptimizerGene)
    persona: PersonaGene = Field(default_factory=PersonaGene)
    aide: AIDEGene = Field(default_factory=AIDEGene)
    governance: GovernanceGene = Field(default_factory=GovernanceGene)

    def canonical_json(self) -> str:
        payload = self.model_dump(mode="json", exclude_none=False)
        return json.dumps(payload, sort_keys=True, separators=(",", ":"))

    def fingerprint(self, length: int = 16) -> str:
        digest = hashlib.sha256(self.canonical_json().encode("utf-8")).hexdigest()
        return digest[:length]

    def child_name(self, mutation_label: str) -> str:
        return f"{self.name}::{mutation_label}"
