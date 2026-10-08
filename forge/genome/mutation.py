from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import Any

from forge.genome.schema import CognitiveGenome


@dataclass(frozen=True)
class Mutation:
    path: str
    value: Any
    rationale: str


def apply_mutations(
    parent: CognitiveGenome, mutations: list[Mutation], *, name: str
) -> CognitiveGenome:
    data = deepcopy(parent.model_dump())
    for mutation in mutations:
        cursor: Any = data
        parts = mutation.path.split(".")
        for part in parts[:-1]:
            if part not in cursor:
                raise KeyError(f"unknown genome path: {mutation.path}")
            cursor = cursor[part]
        if parts[-1] not in cursor:
            raise KeyError(f"unknown genome path: {mutation.path}")
        cursor[parts[-1]] = mutation.value
    data["name"] = name
    data["parent"] = parent.fingerprint()
    return CognitiveGenome.model_validate(data)
