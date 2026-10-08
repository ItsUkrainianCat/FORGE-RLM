from __future__ import annotations

import math
import random
from dataclasses import dataclass

from forge.aide.schema import StrategyArm


@dataclass
class ArmState:
    pulls: int = 0
    total_reward: float = 0.0
    best_reward: float = float("-inf")
    failures: int = 0

    @property
    def mean_reward(self) -> float:
        return self.total_reward / self.pulls if self.pulls else 0.0

    @property
    def failure_rate(self) -> float:
        return self.failures / self.pulls if self.pulls else 0.0


class StrategyBandit:
    """UCB1 portfolio with optional softmax-over-best exploration.

    This preserves diverse search lineages instead of collapsing immediately onto
    the first locally strong strategy.
    """

    def __init__(
        self,
        arms: list[StrategyArm],
        *,
        softmax_probability: float = 0.30,
        temperature: float = 0.5,
        seed: int = 0,
        failure_penalty: float = 0.5,
    ) -> None:
        if not arms:
            raise ValueError("at least one arm is required")
        self.arms = list(arms)
        self.state = {arm: ArmState() for arm in self.arms}
        self.softmax_probability = softmax_probability
        self.temperature = temperature
        self.rng = random.Random(seed)
        self.failure_penalty = failure_penalty

    def update(self, arm: StrategyArm, reward: float, *, buggy: bool = False) -> None:
        s = self.state[arm]
        s.pulls += 1
        s.total_reward += reward
        s.best_reward = max(s.best_reward, reward)
        if buggy:
            s.failures += 1

    def choose(self) -> StrategyArm:
        untried = [arm for arm, s in self.state.items() if s.pulls == 0]
        if untried:
            return self.rng.choice(untried)
        if self.rng.random() < self.softmax_probability:
            return self._softmax_best()
        return self._ucb1()

    def _ucb1(self) -> StrategyArm:
        total_pulls = sum(s.pulls for s in self.state.values())
        return max(
            self.arms,
            key=lambda arm: (
                self.state[arm].mean_reward
                - self.failure_penalty * self.state[arm].failure_rate
                + math.sqrt(2.0 * math.log(total_pulls) / self.state[arm].pulls)
            ),
        )

    def _softmax_best(self) -> StrategyArm:
        raw = [self.state[a].best_reward for a in self.arms]
        finite = [x for x in raw if math.isfinite(x)]
        floor = min(finite) if finite else 0.0
        values = [x if math.isfinite(x) else floor for x in raw]
        m = max(values)
        weights = [math.exp((x - m) / self.temperature) for x in values]
        return self.rng.choices(self.arms, weights=weights, k=1)[0]

    def snapshot(self) -> dict[str, dict[str, float | int]]:
        return {
            arm.value: {
                "pulls": state.pulls,
                "mean_reward": state.mean_reward,
                "best_reward": state.best_reward,
                "failures": state.failures,
                "failure_rate": state.failure_rate,
            }
            for arm, state in self.state.items()
        }
