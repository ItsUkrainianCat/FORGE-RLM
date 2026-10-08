from forge.optimization.pareto import ObjectivePoint, pareto_front


def test_pareto_removes_dominated_point():
    a = ObjectivePoint(name="a", maximize={"quality": 0.9}, minimize={"latency": 1.0})
    b = ObjectivePoint(name="b", maximize={"quality": 0.8}, minimize={"latency": 2.0})
    c = ObjectivePoint(name="c", maximize={"quality": 0.95}, minimize={"latency": 3.0})
    names = {x.name for x in pareto_front([a, b, c])}
    assert "b" not in names
    assert names == {"a", "c"}
