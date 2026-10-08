from __future__ import annotations

import httpx
from pydantic import BaseModel

from forge.aide.receipts import EvaluationReceipt


class GradeRequest(BaseModel):
    candidate_fingerprint: str
    artifact_uri: str
    benchmark_version: str
    budget_fingerprint: str
    run_manifest_fingerprint: str


class SealedEvaluatorClient:
    """Aggregate-only client for a separately hosted private evaluator.

    The service contract intentionally contains no endpoint for listing hidden cases,
    expected outputs, or grader source.
    """

    def __init__(
        self, base_url: str, *, bearer_token: str | None = None, timeout_s: float = 600.0
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout_s = timeout_s
        self.headers = {"Authorization": f"Bearer {bearer_token}"} if bearer_token else {}

    def grade(self, request: GradeRequest) -> EvaluationReceipt:
        response = httpx.post(
            f"{self.base_url}/v1/grade",
            json=request.model_dump(mode="json"),
            headers=self.headers,
            timeout=self.timeout_s,
        )
        response.raise_for_status()
        receipt = EvaluationReceipt.model_validate(response.json())
        if not receipt.verify_digest():
            raise ValueError("evaluator receipt digest failed verification")
        if receipt.candidate_fingerprint != request.candidate_fingerprint:
            raise ValueError("evaluator returned receipt for a different candidate")
        if receipt.benchmark_version != request.benchmark_version:
            raise ValueError("evaluator benchmark version mismatch")
        return receipt
