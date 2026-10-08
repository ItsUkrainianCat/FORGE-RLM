from __future__ import annotations

from pydantic import BaseModel, Field

from forge.security.trust import TrustLevel


class Provenance(BaseModel):
    source: str
    trust: TrustLevel
    evidence_ids: list[str] = Field(default_factory=list)
    independently_validated: bool = False
