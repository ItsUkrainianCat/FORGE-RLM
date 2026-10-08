from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

import dspy

from forge.config import Settings


class RLMTask(dspy.Signature):
    """Solve the query by selectively exploring context; verify important claims and calibrate uncertainty."""

    context: str = dspy.InputField(desc="Potentially large context to inspect programmatically")
    query: str = dspy.InputField()
    answer: str = dspy.OutputField()
    confidence: str = dspy.OutputField(desc="high, medium, low, or unknown")
    evidence_summary: str = dspy.OutputField()
    uncertainties: str = dspy.OutputField()


class ForgeRLM(dspy.Module):
    """Central version-sensitive DSPy RLM wrapper.

    DSPy RLM is experimental. Keep all API assumptions in this file so environment audits can
    patch one adapter instead of the rest of the system.
    """

    def __init__(
        self,
        settings: Settings,
        *,
        sub_lm: dspy.LM | None = None,
        tools: list[Callable] | None = None,
        verbose: bool = False,
    ) -> None:
        super().__init__()
        root_policy_path = Path("prompts/RLM_ROOT.md")
        root_policy = root_policy_path.read_text() if root_policy_path.exists() else ""
        signature = RLMTask.with_instructions((RLMTask.__doc__ or "") + "\n\n" + root_policy)
        if not hasattr(dspy, "RLM"):
            raise RuntimeError("Installed DSPy does not expose dspy.RLM; verify DSPy version/API")
        self.rlm = dspy.RLM(
            signature,
            max_iters=settings.rlm_max_iters,
            max_llm_calls=settings.rlm_max_llm_calls,
            max_output_chars=settings.rlm_max_output_chars,
            verbose=verbose,
            tools=tools or [],
            sub_lm=sub_lm,
        )

    def forward(self, *, context: str, query: str):
        return self.rlm(context=context, query=query)
