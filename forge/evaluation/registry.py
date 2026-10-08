from __future__ import annotations

from forge.evaluation.graders import DEFAULT_GRADERS, Grader


class GraderRegistry:
    def __init__(self) -> None:
        self._graders: dict[str, Grader] = dict(DEFAULT_GRADERS)

    def register(self, name: str, grader: Grader) -> None:
        if name in self._graders:
            raise ValueError(f"grader already registered: {name}")
        self._graders[name] = grader

    def get(self, name: str) -> Grader:
        try:
            return self._graders[name]
        except KeyError as exc:
            raise KeyError(f"unknown grader {name!r}; available={sorted(self._graders)}") from exc

    def names(self) -> list[str]:
        return sorted(self._graders)
