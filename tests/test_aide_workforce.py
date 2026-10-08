from forge.aide.workforce import ResearchJob, ResearchWorkforceScheduler


def test_workforce_penalizes_duplicate_and_slow_work():
    jobs = [
        ResearchJob("clean", expected_value=1.0, compute_cost=1.0),
        ResearchJob("duplicated", expected_value=1.0, compute_cost=1.0, duplicate_risk=2.0),
    ]
    ranked = ResearchWorkforceScheduler().rank(jobs)
    assert ranked[0].job_id == "clean"
