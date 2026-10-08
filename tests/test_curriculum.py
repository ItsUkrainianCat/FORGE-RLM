from forge.curriculum.miner import cluster_failures
from forge.evaluation.schema import CaseResult


def test_failure_clusters_by_tags():
    rows = [
        CaseResult(
            case_id="a",
            score=0,
            passed=False,
            prediction="",
            grader="exact_match",
            tags=["abstraction"],
        ),
        CaseResult(
            case_id="b",
            score=0.5,
            passed=False,
            prediction="",
            grader="exact_match",
            tags=["abstraction"],
        ),
    ]
    clusters = cluster_failures(rows)
    assert clusters[0].key == "abstraction" and clusters[0].count == 2
