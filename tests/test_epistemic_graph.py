from forge.memory.epistemic import ClaimNode, EpistemicGraph, Relation


def test_retraction_propagates_to_dependents():
    g = EpistemicGraph()
    g.add_claim(ClaimNode(id="a", statement="A", confidence=0.9, status="validated"))
    g.add_claim(ClaimNode(id="b", statement="B", confidence=0.8, status="validated"))
    g.link(Relation(source_id="a", target_id="b", relation="depends_on"))
    affected = g.retract_claim("a")
    assert affected == {"a", "b"}
    assert g.claims["b"].status == "retracted"
