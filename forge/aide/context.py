from __future__ import annotations

from dataclasses import dataclass

from forge.aide.archive import CandidateArchive
from forge.aide.schema import AIDEConfig, CandidateNode


@dataclass(frozen=True)
class CompactedContext:
    text: str
    bug_rate: float
    failure_signatures: tuple[str, ...]
    included_node_ids: tuple[str, ...]


class ContextCompactor:
    """Bounded, role-neutral context compaction for long research runs."""

    def __init__(self, config: AIDEConfig) -> None:
        self.config = config

    def build(self, archive: CandidateArchive) -> CompactedContext:
        root = archive.get(archive.root_id)
        recent = archive.recent(self.config.recent_context_nodes)
        nodes: list[CandidateNode] = []
        seen: set[str] = set()
        for node in [root, *recent]:
            if node.node_id not in seen:
                nodes.append(node)
                seen.add(node.node_id)

        bug_rate = archive.bug_rate()
        failures: list[str] = []
        if bug_rate >= self.config.failure_memory_bug_rate_threshold:
            failures = archive.recurring_error_signatures(self.config.failure_memory_max_signatures)

        lines = ["ROOT/RECENT CANDIDATES"]
        for node in nodes:
            score = "n/a" if node.public_score is None else f"{node.public_score:.6f}"
            lines.append(
                f"- {node.node_id} parent={node.parent_id} strategy={node.strategy.value} "
                f"op={node.operator.value} score={score} buggy={node.buggy}: {node.summary[:500]}"
            )
        if failures:
            lines.append("RECURRING FAILURE SIGNATURES")
            lines.extend(f"- {item}" for item in failures)

        return CompactedContext(
            text="\n".join(lines),
            bug_rate=bug_rate,
            failure_signatures=tuple(failures),
            included_node_ids=tuple(n.node_id for n in nodes),
        )
