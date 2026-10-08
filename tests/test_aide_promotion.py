from forge.aide.promotion import NoiseAwarePromotionPolicy, paired_bootstrap_delta_ci
from forge.aide.schema import PrivateGrade


def grade(scores, *, cost=10.0, hacking=0.2, catastrophic=0):
    return PrivateGrade(
        aggregate=sum(scores) / len(scores),
        seed_scores=list(scores),
        compute_cost_units=cost,
        reward_hacking_rate=hacking,
        catastrophic_failures=catastrophic,
    )


def test_paired_bootstrap_detects_uniform_gain():
    delta, lo, hi = paired_bootstrap_delta_ci([0.72, 0.71, 0.73], [0.70, 0.69, 0.71], samples=500)
    assert delta > 0
    assert lo > 0
    assert hi > 0


def test_promotion_requires_robust_gain_and_cost_parity():
    policy = NoiseAwarePromotionPolicy(minimum_seeds=3, confidence=0.9, max_cost_ratio=1.0)
    incumbent = grade([0.70, 0.69, 0.71])
    candidate = grade([0.72, 0.71, 0.73])
    ok, _, _ = policy.evaluate(candidate, incumbent)
    assert ok
    expensive = grade([0.80, 0.79, 0.81], cost=20.0)
    ok, reason, _ = policy.evaluate(expensive, incumbent)
    assert not ok
    assert "cost ratio" in reason


def test_reward_hacking_regression_blocks_promotion():
    policy = NoiseAwarePromotionPolicy(minimum_seeds=3, max_reward_hacking_increase=0.0)
    incumbent = grade([0.70, 0.69, 0.71], hacking=0.1)
    candidate = grade([0.72, 0.71, 0.73], hacking=0.2)
    ok, reason, _ = policy.evaluate(candidate, incumbent)
    assert not ok
    assert "reward-hacking" in reason
