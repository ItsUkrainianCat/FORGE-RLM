from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime

from pydantic import BaseModel, Field

from forge.aide.schema import PrivateGrade


class EvaluationReceipt(BaseModel):
    candidate_fingerprint: str
    benchmark_version: str
    grader_version: str
    budget_fingerprint: str
    grade: PrivateGrade
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    digest: str = ""

    def canonical_payload(self) -> str:
        payload = self.model_dump(mode="json", exclude={"digest"})
        return json.dumps(payload, sort_keys=True, separators=(",", ":"))

    def with_digest(self) -> EvaluationReceipt:
        digest = hashlib.sha256(self.canonical_payload().encode()).hexdigest()
        return self.model_copy(update={"digest": digest})

    def verify_digest(self) -> bool:
        expected = hashlib.sha256(self.canonical_payload().encode()).hexdigest()
        return bool(self.digest) and self.digest == expected
