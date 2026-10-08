from __future__ import annotations

import dspy

from forge.config import Settings


def build_lm(
    settings: Settings, model_id: str | None = None, *, temperature: float | None = None
) -> dspy.LM:
    """Build a DSPy LM against an OpenAI-compatible local endpoint.

    DSPy provider syntax can evolve; verify against the installed DSPy version if this adapter fails.
    """
    chosen = model_id or settings.model_id
    # LiteLLM/DSPy typically uses provider-prefixed model names for OpenAI-compatible APIs.
    # `openai/<id>` is intentionally centralized here so it is easy to change after environment audit.
    model = chosen if "/" in chosen else f"openai/{chosen}"
    return dspy.LM(
        model=model,
        api_base=settings.api_base,
        api_key=settings.api_key,
        temperature=settings.temperature if temperature is None else temperature,
        max_tokens=settings.max_tokens,
    )
