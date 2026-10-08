from forge.aide.ignition import run_ignition_test


def test_ignition_requires_real_outer_loop_improvement():
    def runner(name: str, seed: int):
        if name == "candidate":
            return 0.80 + seed * 0.001, 20
        return 0.77 + seed * 0.001, 35

    report = run_ignition_test(
        treatment_name="candidate",
        reference_name="reference",
        seeds=[1, 2, 3],
        run_outer_loop=runner,
    )
    assert report.promote_to_outer_loop
    assert report.endpoint_delta > 0
    assert report.faster_to_threshold is True
