from __future__ import annotations

from datetime import UTC, datetime

from forge.memory.schema import MemoryRecord


def eligible_for_durable_write(record: MemoryRecord) -> tuple[bool, str]:
    if record.confidence < 0.75:
        return False, "confidence below durable-write threshold"
    if not record.provenance:
        return False, "missing provenance"
    if record.status in {"superseded", "retracted"}:
        return False, f"{record.status} memory should not be written as active"
    if record.expires_at and record.expires_at <= datetime.now(UTC):
        return False, "memory expired"
    return True, "eligible"
