from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ObjectivePoint:
    name: str
    maximize: dict[str, float]
    minimize: dict[str, float]


def dominates(a: ObjectivePoint, b: ObjectivePoint) -> bool:
    if set(a.maximize) != set(b.maximize) or set(a.minimize) != set(b.minimize):
        raise ValueError("objective keys must match")
    no_worse = all(a.maximize[k] >= b.maximize[k] for k in a.maximize) and all(
        a.minimize[k] <= b.minimize[k] for k in a.minimize
    )
    strictly_better = any(a.maximize[k] > b.maximize[k] for k in a.maximize) or any(
        a.minimize[k] < b.minimize[k] for k in a.minimize
    )
    return no_worse and strictly_better


def pareto_front(points: list[ObjectivePoint]) -> list[ObjectivePoint]:
    return [p for p in points if not any(dominates(other, p) for other in points if other is not p)]
