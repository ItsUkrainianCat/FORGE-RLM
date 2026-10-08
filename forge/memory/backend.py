from __future__ import annotations

from typing import Protocol

from forge.memory.schema import MemoryRecord


class MemoryBackend(Protocol):
    def search(self, query: str, *, limit: int = 8) -> list[MemoryRecord]: ...
    def upsert(self, record: MemoryRecord) -> None: ...


class InMemoryBackend:
    def __init__(self) -> None:
        self.records: dict[str, MemoryRecord] = {}

    def search(self, query: str, *, limit: int = 8) -> list[MemoryRecord]:
        terms = set(query.lower().split())
        ranked = sorted(
            self.records.values(),
            key=lambda r: len(terms & set(r.content.lower().split())),
            reverse=True,
        )
        return ranked[:limit]

    def upsert(self, record: MemoryRecord) -> None:
        self.records[record.id] = record
