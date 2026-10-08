from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from forge.routing.compute_governor import ComputeProfile, ComputeSignals, choose_compute_profile


class Route(StrEnum):
    DIRECT = "direct"
    DIRECT_VERIFY = "direct_verify"
    RLM = "rlm"
    RLM_MEMORY = "rlm_memory"
    TOOL = "tool"
    SYNTHESIS = "synthesis"
    MULTI_CANDIDATE = "multi_candidate"
    FORENSIC = "forensic"


@dataclass(frozen=True)
class RouteDecision:
    route: Route
    reason: str
    compute_profile: ComputeProfile = ComputeProfile.BALANCED


def _difficulty(query: str, context_chars: int) -> float:
    q = query.lower()
    score = min(len(query) / 2000.0, 0.35) + min(context_chars / 120_000.0, 0.40)
    if any(
        k in q
        for k in (
            "prove",
            "compare",
            "debug",
            "root cause",
            "architecture",
            "research",
            "many files",
        )
    ):
        score += 0.20
    return min(score, 1.0)


def heuristic_route(
    query: str, *, context_chars: int = 0, consequence_risk: float = 0.0
) -> RouteDecision:
    """Cheap baseline router. A learned router must beat this on held-out routing cases."""
    q = query.lower()
    difficulty = _difficulty(query, context_chars)
    profile = choose_compute_profile(
        ComputeSignals(
            estimated_difficulty=difficulty,
            consequence_risk=consequence_risk,
            context_pressure=min(context_chars / 100_000.0, 1.0),
            ambiguity=0.4 if len(query.split()) < 6 else 0.1,
        )
    )
    if any(k in q for k in ("remember", "previous experiment", "what did we learn", "past run")):
        return RouteDecision(Route.RLM_MEMORY, "durable project memory is relevant", profile)
    if context_chars > 40_000 or any(
        k in q for k in ("many files", "long context", "compare documents")
    ):
        return RouteDecision(Route.RLM, "large/noisy context", profile)
    if any(k in q for k in ("invent", "brainstorm", "name this", "new architecture", "synthesize")):
        return RouteDecision(Route.SYNTHESIS, "novel synthesis requested", profile)
    if any(
        k in q for k in ("run tests", "inspect repo", "search files", "calculate", "query database")
    ):
        return RouteDecision(Route.TOOL, "external tool dominates language-only reasoning", profile)
    if profile == ComputeProfile.FORENSIC:
        return RouteDecision(Route.FORENSIC, "high difficulty/risk", profile)
    if profile == ComputeProfile.DEEP:
        return RouteDecision(Route.RLM, "deep reasoning budget warranted", profile)
    if len(query) < 240 and context_chars < 4_000:
        return RouteDecision(Route.DIRECT, "simple request", profile)
    return RouteDecision(Route.DIRECT_VERIFY, "moderate request", profile)
