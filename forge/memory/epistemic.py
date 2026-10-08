from __future__ import annotations

from collections import defaultdict, deque
from typing import Literal

from pydantic import BaseModel, Field

RelationType = Literal[
    "supports",
    "contradicts",
    "supersedes",
    "derived_from",
    "depends_on",
    "validated_by",
    "failed_under",
]


class EvidenceNode(BaseModel):
    id: str
    content: str
    source: str
    trust: float = Field(ge=0.0, le=1.0)


class ClaimNode(BaseModel):
    id: str
    statement: str
    confidence: float = Field(ge=0.0, le=1.0)
    status: Literal["hypothesis", "validated", "superseded", "retracted"] = "hypothesis"


class Relation(BaseModel):
    source_id: str
    target_id: str
    relation: RelationType


class EpistemicGraph:
    """Backend-independent dependency graph for claim/evidence provenance."""

    def __init__(self) -> None:
        self.evidence: dict[str, EvidenceNode] = {}
        self.claims: dict[str, ClaimNode] = {}
        self.relations: list[Relation] = []
        self._dependents: dict[str, set[str]] = defaultdict(set)

    def add_evidence(self, node: EvidenceNode) -> None:
        self.evidence[node.id] = node

    def add_claim(self, node: ClaimNode) -> None:
        self.claims[node.id] = node

    def link(self, relation: Relation) -> None:
        self.relations.append(relation)
        if relation.relation in {"depends_on", "derived_from", "supports", "validated_by"}:
            self._dependents[relation.source_id].add(relation.target_id)

    def retract_claim(self, claim_id: str) -> set[str]:
        if claim_id not in self.claims:
            raise KeyError(claim_id)
        affected: set[str] = {claim_id}
        queue = deque([claim_id])
        while queue:
            current = queue.popleft()
            for dependent in self._dependents.get(current, set()):
                if dependent not in affected:
                    affected.add(dependent)
                    queue.append(dependent)
        for cid in affected:
            if cid in self.claims:
                self.claims[cid].status = "retracted"
        return affected

    def support_for(self, claim_id: str) -> list[EvidenceNode]:
        ids = [
            r.source_id
            for r in self.relations
            if r.target_id == claim_id and r.relation in {"supports", "validated_by"}
        ]
        return [self.evidence[i] for i in ids if i in self.evidence]
