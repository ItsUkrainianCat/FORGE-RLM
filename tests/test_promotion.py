from forge.controller.promotion import PromotionPolicy, promote_candidate


def test_holdout_required():
    ok, reason = promote_candidate(
        policy=PromotionPolicy(),
        dev_delta=0.05,
        holdout_delta=None,
        latency_ratio=1.0,
        critical_regressions=0,
        catastrophic_failures=0,
    )
    assert not ok and "holdout" in reason


def test_good_candidate_promotes():
    ok, _ = promote_candidate(
        policy=PromotionPolicy(),
        dev_delta=0.05,
        holdout_delta=0.03,
        latency_ratio=1.2,
        critical_regressions=0,
        catastrophic_failures=0,
    )
    assert ok
