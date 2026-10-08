from __future__ import annotations

from forge.aide.schema import CandidateNode, StrategyArm


class CandidateArchive:
    """Append-only candidate tree used by the inner research loop."""

    def __init__(self, root: CandidateNode) -> None:
        if root.parent_id is not None:
            raise ValueError("root must not have a parent")
        self._nodes: dict[str, CandidateNode] = {root.node_id: root}
        self._order: list[str] = [root.node_id]
        self.root_id = root.node_id

    def add(self, node: CandidateNode) -> None:
        if node.node_id in self._nodes:
            raise ValueError(f"duplicate node id: {node.node_id}")
        if node.parent_id not in self._nodes:
            raise ValueError(f"unknown parent: {node.parent_id}")
        self._nodes[node.node_id] = node
        self._order.append(node.node_id)

    def get(self, node_id: str) -> CandidateNode:
        return self._nodes[node_id]

    def all(self) -> list[CandidateNode]:
        return [self._nodes[node_id] for node_id in self._order]

    def recent(self, n: int) -> list[CandidateNode]:
        return [self._nodes[node_id] for node_id in self._order[-n:]]

    def scored(self) -> list[CandidateNode]:
        return [n for n in self.all() if n.public_score is not None and not n.buggy]

    def best(self) -> CandidateNode:
        scored = self.scored()
        if not scored:
            return self.get(self.root_id)
        return max(scored, key=lambda n: float(n.public_score))

    def best_for_arm(self, arm: StrategyArm) -> CandidateNode | None:
        candidates = [n for n in self.scored() if n.strategy == arm]
        return max(candidates, key=lambda n: float(n.public_score)) if candidates else None

    def bug_rate(self) -> float:
        nodes = self.all()[1:]
        return sum(1 for n in nodes if n.buggy) / len(nodes) if nodes else 0.0

    def recurring_error_signatures(self, max_items: int = 3) -> list[str]:
        counts: dict[str, int] = {}
        for node in self.all():
            if node.error_signature:
                signature = node.error_signature.strip()
                if signature:
                    counts[signature] = counts.get(signature, 0) + 1
        ranked = sorted(counts.items(), key=lambda pair: (-pair[1], pair[0]))
        return [signature for signature, _ in ranked[:max_items]]
