from forge.aide.sequential import sequential_promotion_decision


def test_sequential_accepts_clear_gain():
    d = sequential_promotion_decision([0.73, 0.74, 0.72], [0.70, 0.71, 0.69], min_seeds=3)
    assert d.decision == "accept"


def test_sequential_rejects_clear_loss():
    d = sequential_promotion_decision([0.68, 0.69, 0.67], [0.70, 0.71, 0.69], min_seeds=3)
    assert d.decision == "reject"
