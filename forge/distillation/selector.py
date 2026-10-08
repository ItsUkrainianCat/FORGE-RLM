from __future__ import annotations

import json
from pathlib import Path

from forge.distillation.trajectory import TrajectoryRecord


def select_trajectories(
    records: list[TrajectoryRecord], *, min_score: float = 0.95, max_latency_ms: float | None = None
) -> list[TrajectoryRecord]:
    selected = []
    for record in records:
        if record.score < min_score:
            continue
        if not record.provenance:
            continue
        if max_latency_ms is not None and record.latency_ms > max_latency_ms:
            continue
        selected.append(record)
    return selected


def export_sft_jsonl(records: list[TrajectoryRecord], path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as fh:
        for record in records:
            row = {
                "messages": [
                    {"role": "user", "content": record.query},
                    {"role": "assistant", "content": record.answer},
                ],
                "metadata": {
                    "trajectory_id": record.id,
                    "score": record.score,
                    "genome": record.genome_fingerprint,
                    "tags": record.tags,
                },
            }
            fh.write(json.dumps(row) + "\n")
    return path
