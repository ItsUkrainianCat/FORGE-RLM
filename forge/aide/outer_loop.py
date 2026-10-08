from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Generic, TypeVar

from forge.aide.private_grader import EvaluationAuthority
from forge.aide.promotion import NoiseAwarePromotionPolicy
from forge.aide.schema import ImprovementProposal, OuterLoopRecord, PrivateGrade
from forge.aide.scope import ScopePolicy

CandidateT = TypeVar("CandidateT")
ProposalFn = Callable[[CandidateT, list[OuterLoopRecord], str], ImprovementProposal]
BuildFn = Callable[[CandidateT, ImprovementProposal], CandidateT]
FingerprintFn = Callable[[CandidateT], str]


@dataclass
class OuterLoopResult(Generic[CandidateT]):
    incumbent: CandidateT
    incumbent_grade: PrivateGrade
    records: list[OuterLoopRecord]
    accepted_rewrites: int


class OuterLoopImprover(Generic[CandidateT]):
    """Meta-level optimizer over the research agent/harness itself."""

    def __init__(
        self,
        *,
        evaluator: EvaluationAuthority[CandidateT],
        promotion: NoiseAwarePromotionPolicy,
        scope: ScopePolicy | None = None,
    ) -> None:
        self.evaluator = evaluator
        self.promotion = promotion
        self.scope = scope or ScopePolicy()

    def run(
        self,
        *,
        initial: CandidateT,
        propose: ProposalFn[CandidateT],
        build: BuildFn[CandidateT],
        fingerprint: FingerprintFn[CandidateT],
        target_failure: str,
        steps: int,
    ) -> OuterLoopResult[CandidateT]:
        incumbent = initial
        incumbent_grade = self.evaluator.grade(incumbent)
        records: list[OuterLoopRecord] = []
        accepted = 0

        for step in range(1, steps + 1):
            proposal = propose(incumbent, list(records), target_failure)
            ok, problems = self.scope.validate_manifest(proposal.patch)
            if not ok:
                candidate_id = f"invalid:{proposal.proposal_id}"
                records.append(
                    OuterLoopRecord(
                        step=step,
                        proposal_id=proposal.proposal_id,
                        parent_genome=fingerprint(incumbent),
                        candidate_genome=candidate_id,
                        accepted=False,
                        incumbent_before=incumbent_grade.aggregate,
                        candidate_grade=float("-inf"),
                        incumbent_after=incumbent_grade.aggregate,
                        rationale="scope rejection: " + "; ".join(problems),
                        grade=PrivateGrade(
                            aggregate=float("-1e9"),
                            seed_scores=[float("-1e9")] * self.promotion.minimum_seeds,
                            catastrophic_failures=1,
                        ),
                    )
                )
                continue

            candidate = build(incumbent, proposal)
            candidate_grade = self.evaluator.grade(candidate)
            promote, reason, details = self.promotion.evaluate(candidate_grade, incumbent_grade)
            before = incumbent_grade.aggregate
            if promote:
                incumbent = candidate
                incumbent_grade = candidate_grade
                accepted += 1
            records.append(
                OuterLoopRecord(
                    step=step,
                    proposal_id=proposal.proposal_id,
                    parent_genome=proposal.parent_genome,
                    candidate_genome=fingerprint(candidate),
                    accepted=promote,
                    incumbent_before=before,
                    candidate_grade=candidate_grade.aggregate,
                    incumbent_after=incumbent_grade.aggregate,
                    rationale=f"{reason}; details={details}",
                    grade=candidate_grade,
                )
            )

        return OuterLoopResult(
            incumbent=incumbent,
            incumbent_grade=incumbent_grade,
            records=records,
            accepted_rewrites=accepted,
        )
