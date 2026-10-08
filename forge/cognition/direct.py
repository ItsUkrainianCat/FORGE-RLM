from __future__ import annotations

import dspy


class DirectAnswer(dspy.Signature):
    """Answer accurately and directly; use context when provided and calibrate unsupported claims."""

    query: str = dspy.InputField()
    context: str = dspy.InputField(default="")
    answer: str = dspy.OutputField()


class DirectProgram(dspy.Module):
    def __init__(self) -> None:
        super().__init__()
        self.predict = dspy.Predict(DirectAnswer)

    def forward(self, query: str, context: str = ""):
        return self.predict(query=query, context=context)
