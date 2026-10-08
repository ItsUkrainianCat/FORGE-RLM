from __future__ import annotations

from collections.abc import Callable
from typing import Protocol, TypeVar

from forge.aide.schema import PrivateGrade

CandidateT = TypeVar("CandidateT")


class PrivateGrader(Protocol[CandidateT]):
    def __call__(self, candidate: CandidateT) -> PrivateGrade: ...


class EvaluationAuthority:
    """Boundary object for private evaluation.

    The proposal/search agent receives only the returned aggregate decision/reason,
    never the sealed examples, expected outputs, or grader implementation.
    """

    def __init__(self, grader: Callable[[CandidateT], PrivateGrade]) -> None:
        self._grader = grader

    def grade(self, candidate: CandidateT) -> PrivateGrade:
        return self._grader(candidate)
