from __future__ import annotations

import dspy

from forge.verification.pipeline import VerificationResult


class VerifyAnswer(dspy.Signature):
    """Independently verify an answer. PASS if sound; otherwise give precise revision feedback."""

    query: str = dspy.InputField()
    answer: str = dspy.InputField()
    evidence: str = dspy.InputField(default="")
    verdict: str = dspy.OutputField(desc="PASS or REVISE")
    feedback: str = dspy.OutputField()


class Verifier(dspy.Module):
    name = "lm_critic"

    def __init__(self) -> None:
        super().__init__()
        self.predict = dspy.Predict(VerifyAnswer)

    def forward(self, query: str, answer: str, evidence: str = ""):
        return self.predict(query=query, answer=answer, evidence=evidence)

    def verify(self, *, query: str, answer: str, evidence: str = "") -> VerificationResult:
        result = self.forward(query=query, answer=answer, evidence=evidence)
        verdict = str(getattr(result, "verdict", "REVISE")).strip().upper()
        passed = verdict.startswith("PASS")
        return VerificationResult(
            passed=passed,
            stage=self.name,
            feedback=str(getattr(result, "feedback", "")),
            score=1.0 if passed else 0.0,
        )
