from __future__ import annotations

import json
from pathlib import Path

import dspy

from forge.aide.schema import ImprovementProposal, PatchManifest


class OuterResearchProposal(dspy.Signature):
    """Propose one minimal, falsifiable harness improvement. Never alter sealed evaluation or permissions."""

    incumbent_summary: str = dspy.InputField()
    failure_cluster: str = dspy.InputField()
    experiment_history: str = dspy.InputField()
    proposal_json: str = dspy.OutputField(desc="JSON matching ImprovementProposal")


class DSPyOuterLoopProposer(dspy.Module):
    """Optional model-backed proposal generator used after endpoint/API audit."""

    def __init__(self) -> None:
        super().__init__()
        policy_path = Path("prompts/AIDE_OUTER_LOOP.md")
        policy = policy_path.read_text() if policy_path.exists() else ""
        signature = OuterResearchProposal.with_instructions(
            (OuterResearchProposal.__doc__ or "") + "\n\n" + policy
        )
        self.predictor = dspy.Predict(signature)

    def forward(
        self, *, incumbent_summary: str, failure_cluster: str, experiment_history: str
    ) -> ImprovementProposal:
        prediction = self.predictor(
            incumbent_summary=incumbent_summary,
            failure_cluster=failure_cluster,
            experiment_history=experiment_history,
        )
        payload = json.loads(prediction.proposal_json)
        if "patch" not in payload:
            payload["patch"] = PatchManifest().model_dump(mode="json")
        return ImprovementProposal.model_validate(payload)
