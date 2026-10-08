from forge.memory.policy import eligible_for_durable_write
from forge.memory.schema import MemoryRecord


def test_memory_requires_provenance():
    record = MemoryRecord(
        id="x", category="semantic", content="claim", source="model", confidence=0.9
    )
    ok, _ = eligible_for_durable_write(record)
    assert not ok


def test_validated_memory_can_write():
    record = MemoryRecord(
        id="x",
        category="evidence",
        content="measured",
        source="eval",
        confidence=0.95,
        provenance=["experiment-1"],
        status="validated",
    )
    ok, _ = eligible_for_durable_write(record)
    assert ok
