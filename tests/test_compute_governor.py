from forge.routing.compute_governor import ComputeProfile, ComputeSignals, choose_compute_profile


def test_fast_for_easy_task():
    assert choose_compute_profile(ComputeSignals(estimated_difficulty=0.05)) == ComputeProfile.FAST


def test_forensic_for_high_risk_hard_task():
    p = choose_compute_profile(
        ComputeSignals(
            estimated_difficulty=1.0, consequence_risk=1.0, context_pressure=1.0, ambiguity=1.0
        )
    )
    assert p == ComputeProfile.FORENSIC
