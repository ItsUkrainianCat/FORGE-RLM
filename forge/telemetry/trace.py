from __future__ import annotations

import json
import uuid
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field


class TraceEvent(BaseModel):
    trace_id: str
    event: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    data: dict[str, Any] = Field(default_factory=dict)


class TraceWriter:
    def __init__(self, directory: str | Path = "artifacts/traces") -> None:
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def new_trace_id() -> str:
        return uuid.uuid4().hex

    def write(self, event: TraceEvent) -> None:
        path = self.directory / f"{event.trace_id}.jsonl"
        with path.open("a") as fh:
            fh.write(json.dumps(event.model_dump(mode="json"), default=str) + "\n")
