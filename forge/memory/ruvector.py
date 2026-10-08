from __future__ import annotations

from dataclasses import dataclass

from forge.memory.schema import MemoryRecord


@dataclass(frozen=True)
class RuVectorConfig:
    endpoint: str | None = None
    namespace: str = "forge"


class RuVectorAdapter:
    """Version-sensitive integration boundary.

    Ruflo/RuVector expose multiple surfaces (plugins, MCP, CLI, HTTP/native packages depending on
    installation). Do not guess one here. Environment-specific integration should implement these
    methods after inspecting installed tooling and keep provenance metadata intact.
    """

    def __init__(self, config: RuVectorConfig) -> None:
        self.config = config

    def search(self, query: str, *, limit: int = 8) -> list[MemoryRecord]:
        raise NotImplementedError("bind to the installed RuVector surface after environment audit")

    def upsert(self, record: MemoryRecord) -> None:
        raise NotImplementedError("bind to the installed RuVector surface after environment audit")
