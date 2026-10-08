from __future__ import annotations

import json
from pathlib import Path

from forge.evaluation.schema import EvalCase


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def load_cases(path: Path) -> list[EvalCase]:
    return [EvalCase.model_validate(row) for row in load_jsonl(path)]
