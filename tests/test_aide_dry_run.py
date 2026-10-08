from forge.aide.dry_run import run_dry_run


def test_dry_run_demonstrates_accept_reject_lineage():
    result = run_dry_run(steps=5)
    assert result["accepted_rewrites"] >= 1
    decisions = [row["accepted"] for row in result["records"]]
    assert any(decisions)
    assert any(not d for d in decisions)
