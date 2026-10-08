from __future__ import annotations

from dataclasses import dataclass

from forge.aide.schema import ImprovementProposal
from forge.genome.mutation import Mutation, apply_mutations
from forge.genome.schema import CognitiveGenome


@dataclass(frozen=True)
class GenomeMutationScope:
    """Self-referential mutation surface for CognitiveGenome genes.

    Compute budgets, model identity, permissions, evaluator secrecy, ignition, and
    governance are deliberately not mutable by the autonomous outer loop.
    """

    allowed_prefixes: tuple[str, ...] = (
        "inference.temperature",
        "inference.top_p",
        "inference.max_tokens",
        "inference.reasoning_mode",
        "router.version",
        "router.direct_threshold",
        "router.deep_threshold",
        "rlm.enabled",
        "rlm.max_iters",
        "rlm.max_llm_calls",
        "rlm.max_output_chars",
        "verification.enabled",
        "verification.stages",
        "verification.max_revisions",
        "memory.enabled",
        "memory.backend",
        "memory.retrieval_k",
        "memory.policy",
        "tools.router",
        "optimizer.dspy_program",
        "optimizer.gepa_candidate",
        "persona.enabled",
        "persona.version",
        "aide.strategy_policy",
    )

    def validate(self, path: str) -> tuple[bool, str]:
        if path.startswith("governance."):
            return False, "governance genes are protected"
        if path in {
            "model.model_id",
            "model.quantization",
            "model.context_length",
            "tools.allowed_domains",
            "aide.outer_steps",
            "aide.fixed_budget",
            "aide.sealed_private_grading",
            "aide.ignition_required",
        }:
            return (
                False,
                "gene changes research budget, authority, permissions, or model generation",
            )
        if path in self.allowed_prefixes:
            return True, "allowed"
        return False, f"gene outside autonomous mutation surface: {path}"


def apply_proposal_to_genome(
    parent: CognitiveGenome,
    proposal: ImprovementProposal,
    *,
    scope: GenomeMutationScope | None = None,
) -> CognitiveGenome:
    scope = scope or GenomeMutationScope()
    mutations: list[Mutation] = []
    for spec in proposal.genome_mutations:
        ok, reason = scope.validate(spec.path)
        if not ok:
            raise PermissionError(f"{spec.path}: {reason}")
        mutations.append(Mutation(path=spec.path, value=spec.value, rationale=spec.rationale))
    if not mutations:
        # Code/prompt-only proposals may leave genome values unchanged but still need a child identity.
        data = parent.model_copy(deep=True)
        payload = data.model_dump()
        payload["name"] = parent.child_name(proposal.mutation_label)
        payload["parent"] = parent.fingerprint()
        return CognitiveGenome.model_validate(payload)
    return apply_mutations(parent, mutations, name=parent.child_name(proposal.mutation_label))
