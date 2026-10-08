from forge.aide.reward_hacking import ProxyDownstreamCase, evaluate_proxy_downstream


def test_proxy_downstream_hacking_rate():
    report = evaluate_proxy_downstream(
        [
            ProxyDownstreamCase(case_id="a", proxy_gain=1.0, downstream_gain=-0.1),
            ProxyDownstreamCase(case_id="b", proxy_gain=1.0, downstream_gain=0.5),
        ]
    )
    assert report.hacking_cases == 1
    assert report.rate == 0.5
