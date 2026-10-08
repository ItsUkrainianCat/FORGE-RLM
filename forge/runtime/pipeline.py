from __future__ import annotations

import time
from collections.abc import Callable
from dataclasses import dataclass

from forge.routing.router import Route, heuristic_route
from forge.runtime.envelope import PredictionEnvelope


@dataclass
class RuntimeComponents:
    direct: Callable[[str, str], str]
    verify: Callable[[str, str, str], tuple[bool, str]] | None = None
    rlm: Callable[[str, str], object] | None = None
    memory_retrieve: Callable[[str], list[str]] | None = None


class ForgeRuntime:
    def __init__(self, components: RuntimeComponents) -> None:
        self.components = components

    def predict(
        self, *, query: str, context: str = "", consequence_risk: float = 0.0
    ) -> PredictionEnvelope:
        start = time.perf_counter()
        decision = heuristic_route(
            query, context_chars=len(context), consequence_risk=consequence_risk
        )
        answer = ""
        confidence = "unknown"
        evidence: list[str] = []

        if decision.route in {Route.RLM, Route.FORENSIC, Route.RLM_MEMORY} and self.components.rlm:
            if decision.route == Route.RLM_MEMORY and self.components.memory_retrieve:
                evidence = self.components.memory_retrieve(query)
                context = context + "\n\nRETRIEVED MEMORY:\n" + "\n".join(evidence)
            result = self.components.rlm(context, query)
            answer = getattr(result, "answer", str(result))
            confidence = getattr(result, "confidence", "unknown")
        else:
            answer = self.components.direct(query, context)

        if decision.route in {Route.DIRECT_VERIFY, Route.FORENSIC} and self.components.verify:
            passed, feedback = self.components.verify(query, answer, "\n".join(evidence))
            if not passed:
                # One bounded revision request; richer revision policy belongs in verifier pipeline.
                revised_query = f"{query}\n\nVerifier feedback: {feedback}\nRevise the answer once."
                answer = self.components.direct(revised_query, context)

        latency_ms = (time.perf_counter() - start) * 1000
        return PredictionEnvelope(
            answer=answer,
            route=decision.route.value,
            confidence=confidence,
            latency_ms=latency_ms,
            evidence=evidence,
            metadata={
                "compute_profile": decision.compute_profile.value,
                "route_reason": decision.reason,
            },
        )
