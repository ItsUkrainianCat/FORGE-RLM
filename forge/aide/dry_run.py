from __future__ import annotations

from dataclasses import dataclass, replace

from forge.aide.config import load_aide_config
from forge.aide.governance import PauseController
from forge.aide.outer_loop import OuterLoopImprover
from forge.aide.private_grader import EvaluationAuthority
from forge.aide.promotion import NoiseAwarePromotionPolicy
from forge.aide.schema import ImprovementProposal, PatchManifest, PatchOperation, PrivateGrade


@dataclass(frozen=True)
class ToyResearchAgent:
    name: str
    capability: float
    cost: float = 10.0
    reward_hacking: float = 0.20

    def fingerprint(self) -> str:
        return f"{self.name}:{self.capability:.4f}:{self.cost:.2f}:{self.reward_hacking:.3f}"


def run_dry_run(steps: int = 5) -> dict:
    cfg, policy = load_aide_config()
    seed_offsets = (-0.006, 0.0, 0.005)

    def grader(agent: ToyResearchAgent) -> PrivateGrade:
        seeds = [agent.capability + offset for offset in seed_offsets]
        return PrivateGrade(
            aggregate=sum(seeds) / len(seeds),
            seed_scores=seeds,
            task_scores={"toy-rd": sum(seeds) / len(seeds)},
            reward_hacking_rate=agent.reward_hacking,
            compute_cost_units=agent.cost,
        )

    def propose(agent: ToyResearchAgent, history, target: str) -> ImprovementProposal:
        step = len(history) + 1
        return ImprovementProposal(
            proposal_id=f"toy-{step}",
            parent_genome=agent.fingerprint(),
            mutation_label=f"capability-step-{step}",
            target_failure_cluster=target,
            hypothesis="A narrow harness change should improve toy research efficiency at fixed cost.",
            expected_effect="Small capability improvement without reward-hacking increase.",
            patch=PatchManifest(
                operations=[
                    PatchOperation(
                        path="forge/routing/router.py",
                        operation="modify",
                        rationale="toy mutation inside allowed harness scope",
                    )
                ]
            ),
        )

    def build(agent: ToyResearchAgent, proposal: ImprovementProposal) -> ToyResearchAgent:
        step = int(proposal.proposal_id.split("-")[-1])
        # Deterministic mix of useful and bad proposals demonstrates accept/reject behavior.
        gains = {1: 0.015, 2: -0.010, 3: 0.012, 4: 0.004, 5: 0.020}
        gain = gains.get(step, 0.001)
        return replace(agent, name=f"toy-agent-{step}", capability=agent.capability + gain)

    outer = OuterLoopImprover(
        evaluator=EvaluationAuthority(grader),
        promotion=NoiseAwarePromotionPolicy(
            confidence=cfg.promotion_confidence,
            min_delta=cfg.min_private_delta,
            minimum_seeds=cfg.minimum_seeds_for_promotion,
            max_cost_ratio=1.0,
            require_reward_hacking_check=True,
        ),
    )
    pause = PauseController(".forge/DRY_RUN_PAUSED")
    pause.path.unlink(missing_ok=True)
    result = outer.run(
        initial=ToyResearchAgent(name="toy-agent-0", capability=0.70),
        propose=propose,
        build=build,
        fingerprint=lambda x: x.fingerprint(),
        target_failure="toy research efficiency",
        steps=steps,
    )
    return {
        "accepted_rewrites": result.accepted_rewrites,
        "final_agent": result.incumbent.fingerprint(),
        "final_grade": result.incumbent_grade.aggregate,
        "records": [record.model_dump(mode="json") for record in result.records],
        "monitor_policy": policy.__dict__,
    }
