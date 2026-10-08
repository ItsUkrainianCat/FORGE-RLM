from __future__ import annotations

from difflib import SequenceMatcher


def exact_match(pred: str, expected: str) -> float:
    return float(pred.strip().casefold() == expected.strip().casefold())


def repetition_similarity(current: str, previous: str) -> float:
    return SequenceMatcher(None, current.casefold(), previous.casefold()).ratio()
