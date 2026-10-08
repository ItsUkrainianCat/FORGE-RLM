from __future__ import annotations

import time
from dataclasses import dataclass

from forge.aide.schema import BudgetUsage, ResearchBudget


class BudgetExceeded(RuntimeError):
    pass


@dataclass
class BudgetLedger:
    budget: ResearchBudget

    def __post_init__(self) -> None:
        self._start = time.monotonic()
        self._steps = 0
        self._model_calls = 0
        self._cost_units = 0.0

    def usage(self) -> BudgetUsage:
        return BudgetUsage(
            steps=self._steps,
            model_calls=self._model_calls,
            cost_units=self._cost_units,
            wall_time_s=time.monotonic() - self._start,
        )

    def can_spend(self, *, steps: int = 0, model_calls: int = 0, cost_units: float = 0.0) -> bool:
        u = self.usage()
        return (
            u.steps + steps <= self.budget.max_steps
            and u.model_calls + model_calls <= self.budget.max_model_calls
            and u.cost_units + cost_units <= self.budget.max_cost_units
            and u.wall_time_s <= self.budget.max_wall_time_s
        )

    def spend(self, *, steps: int = 0, model_calls: int = 0, cost_units: float = 0.0) -> None:
        if not self.can_spend(steps=steps, model_calls=model_calls, cost_units=cost_units):
            raise BudgetExceeded("research budget exhausted")
        self._steps += steps
        self._model_calls += model_calls
        self._cost_units += cost_units
