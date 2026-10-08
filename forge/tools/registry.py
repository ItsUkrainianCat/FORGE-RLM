from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from enum import StrEnum
from typing import Any


class ToolPermission(StrEnum):
    READ_ONLY = "read_only"
    SIDE_EFFECT = "side_effect"
    PRIVILEGED = "privileged"


@dataclass(frozen=True)
class ToolSpec:
    name: str
    domain: str
    description: str
    fn: Callable[..., Any]
    permission: ToolPermission = ToolPermission.READ_ONLY
    trust_level: str = "bounded"
    cost_hint: float = 0.0
    latency_hint_ms: float = 0.0

    @property
    def requires_approval(self) -> bool:
        return self.permission != ToolPermission.READ_ONLY


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, ToolSpec] = {}

    def register(self, spec: ToolSpec) -> None:
        if spec.name in self._tools:
            raise ValueError(f"duplicate tool: {spec.name}")
        self._tools[spec.name] = spec

    def get(self, name: str) -> ToolSpec:
        return self._tools[name]

    def by_domain(self, domain: str) -> list[ToolSpec]:
        return [x for x in self._tools.values() if x.domain == domain]

    def exposed(
        self, *, allow_side_effects: bool = False, allow_privileged: bool = False
    ) -> list[ToolSpec]:
        allowed = {ToolPermission.READ_ONLY}
        if allow_side_effects:
            allowed.add(ToolPermission.SIDE_EFFECT)
        if allow_privileged:
            allowed.add(ToolPermission.PRIVILEGED)
        return [x for x in self._tools.values() if x.permission in allowed]
