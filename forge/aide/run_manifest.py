from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime

from pydantic import BaseModel, Field

from forge.aide.schema import ResearchBudget


class ResearchRunManifest(BaseModel):
    run_id: str
    incumbent_fingerprint: str
    model_id: str
    benchmark_version: str
    public_signal_version: str
    private_grader_version: str
    budget: ResearchBudget
    seeds: list[int]
    autonomous: bool = False
    network_enabled: bool = False
    mutation_scope_version: str = "harness-only-v1"
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    def fingerprint(self) -> str:
        raw = json.dumps(self.model_dump(mode="json"), sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(raw.encode()).hexdigest()[:20]
