from __future__ import annotations

import dspy

from forge.cognition.direct import DirectProgram
from forge.config import Settings
from forge.models.openai_compat import build_lm
from forge.rlm.core import ForgeRLM
from forge.runtime.pipeline import ForgeRuntime, RuntimeComponents
from forge.verification.verifier import Verifier


def build_runtime(settings: Settings | None = None) -> ForgeRuntime:
    """Build the first functional Qwen-backed FORGE runtime.

    This intentionally centralizes DSPy global configuration. More sophisticated per-module LM
    routing should only be added after the baseline is measured.
    """
    settings = settings or Settings()
    root_lm = build_lm(settings)
    sub_lm = build_lm(settings, settings.sub_model, temperature=max(settings.temperature, 0.2))
    dspy.configure(lm=root_lm)

    direct_program = DirectProgram()
    rlm_program = ForgeRLM(settings, sub_lm=sub_lm)
    verifier = Verifier()

    def direct(query: str, context: str) -> str:
        result = direct_program(query=query, context=context)
        return str(result.answer)

    def rlm(context: str, query: str):
        return rlm_program(context=context, query=query)

    def verify(query: str, answer: str, evidence: str) -> tuple[bool, str]:
        result = verifier.verify(query=query, answer=answer, evidence=evidence)
        return result.passed, result.feedback

    return ForgeRuntime(RuntimeComponents(direct=direct, verify=verify, rlm=rlm))
