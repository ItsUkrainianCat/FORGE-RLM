from forge.evaluation.graders import contains, exact_match, json_valid
from forge.evaluation.schema import EvalCase


def test_exact_match_normalizes_whitespace_case():
    c = EvalCase(id="x", query="q", expected="Hello World", grader="exact_match")
    assert exact_match(c, " hello   world ").passed


def test_contains_multiple_requirements():
    c = EvalCase(id="x", query="q", expected=["alpha", "beta"], grader="contains")
    assert contains(c, "Alpha then beta").passed


def test_json_valid_keys():
    c = EvalCase(id="x", query="q", expected=["answer", "confidence"], grader="json_valid")
    assert json_valid(c, '{"answer":1,"confidence":"high"}').passed
