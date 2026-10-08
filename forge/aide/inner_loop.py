from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from forge.aide.archive import CandidateArchive
from forge.aide.bandit import StrategyBandit
from forge.aide.budget import BudgetLedger
from forge.aide.context import ContextCompactor
from forge.aide.schema import (
    AIDEConfig,
    CandidateNode,
    CandidateProposal,
    CandidateStatus,
    OperatorKind,
    PublicEvaluation,
    ResearchBudget,
    StrategyArm,
)

ProposalFn = Callable[[CandidateNode, StrategyArm, OperatorKind, str], CandidateProposal]
PublicEvaluator = Callable[[str], PublicEvaluation]


@dataclass
class InnerLoopResult:
    best: CandidateNode
    archive: CandidateArchive
    bandit_state: dict
    budget_usage: dict


class InnerLoopResearchAgent:
    """Fixed-budget tree search over task solutions.

    Public feedback is visible here. Private selection grades are intentionally not.
    """

    def __init__(self, config: AIDEConfig, *, seed: int = 0) -> None:
        self.config = config
        self.seed = seed

    def run(
        self,
        *,
        root_artifact_ref: str,
        proposal_fn: ProposalFn,
        public_evaluator: PublicEvaluator,
        budget: ResearchBudget,
    ) -> InnerLoopResult:
        root_eval = public_evaluator(root_artifact_ref)
        root = CandidateNode(
            node_id="root",
            parent_id=None,
            strategy=self.config.strategy_arms[0],
            operator=OperatorKind.AUDIT,
            artifact_ref=root_artifact_ref,
            summary="initial task artifact",
            public_score=root_eval.score,
            public_feedback=root_eval.feedback,
            buggy=root_eval.buggy,
            error_signature=root_eval.error_signature,
            status=CandidateStatus.BUGGY if root_eval.buggy else CandidateStatus.SCORED,
        )
        archive = CandidateArchive(root)
        bandit = StrategyBandit(
            self.config.strategy_arms,
            softmax_probability=self.config.softmax_exploration_probability,
            temperature=self.config.softmax_temperature,
            seed=self.seed,
        )
        ledger = BudgetLedger(budget)
        compactor = ContextCompactor(self.config)

        step = 0
        while ledger.can_spend(steps=1, model_calls=1, cost_units=0.0):
            step += 1
            arm = bandit.choose()
            if step % self.config.fork_every_steps == 0:
                parent = archive.best()
                # Fork the champion under a different strategy when possible.
                alternatives = [a for a in self.config.strategy_arms if a != parent.strategy]
                if alternatives:
                    arm = alternatives[
                        (step // self.config.fork_every_steps - 1) % len(alternatives)
                    ]
            else:
                parent = archive.best_for_arm(arm) or archive.best()

            operator = (
                OperatorKind.DEBUG
                if parent.buggy
                else (
                    OperatorKind.DRAFT
                    if parent.node_id == "root" and step <= len(self.config.strategy_arms)
                    else OperatorKind.IMPROVE
                )
            )
            compacted = compactor.build(archive)
            proposal = proposal_fn(parent, arm, operator, compacted.text)
            if len(proposal.summary.strip()) < self.config.min_candidate_chars:
                # Count the attempt but do not let empty/stub proposals silently enter the archive.
                ledger.spend(
                    steps=1, model_calls=proposal.model_calls, cost_units=proposal.cost_units
                )
                continue
            evaluation = public_evaluator(proposal.artifact_ref)
            node = CandidateNode(
                node_id=f"n{step:04d}",
                parent_id=parent.node_id,
                strategy=arm,
                operator=operator,
                artifact_ref=proposal.artifact_ref,
                summary=proposal.summary,
                public_score=evaluation.score,
                public_feedback=evaluation.feedback,
                buggy=evaluation.buggy,
                error_signature=evaluation.error_signature,
                status=CandidateStatus.BUGGY if evaluation.buggy else CandidateStatus.SCORED,
                metadata=proposal.metadata,
            )
            archive.add(node)
            reward = evaluation.score - (parent.public_score or 0.0)
            if evaluation.buggy:
                reward -= 1.0
            bandit.update(arm, reward, buggy=evaluation.buggy)
            ledger.spend(steps=1, model_calls=proposal.model_calls, cost_units=proposal.cost_units)

        best = archive.best().model_copy(update={"status": CandidateStatus.SELECTED})
        return InnerLoopResult(
            best=best,
            archive=archive,
            bandit_state=bandit.snapshot(),
            budget_usage=ledger.usage().model_dump(),
        )
