from forge.aide.receipts import EvaluationReceipt
from forge.aide.schema import PrivateGrade


def test_evaluation_receipt_digest_detects_tampering():
    receipt = EvaluationReceipt(
        candidate_fingerprint="abc",
        benchmark_version="b1",
        grader_version="g1",
        budget_fingerprint="budget1",
        grade=PrivateGrade(aggregate=0.7, seed_scores=[0.7, 0.71, 0.69]),
    ).with_digest()
    assert receipt.verify_digest()
    changed = receipt.model_copy(update={"candidate_fingerprint": "evil"})
    assert not changed.verify_digest()
