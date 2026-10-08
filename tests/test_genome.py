from forge.genome.mutation import Mutation, apply_mutations
from forge.genome.schema import CognitiveGenome


def test_genome_fingerprint_is_stable():
    g1 = CognitiveGenome(name="a")
    g2 = CognitiveGenome(name="a")
    assert g1.fingerprint() == g2.fingerprint()


def test_mutation_sets_parent_and_changes_fingerprint():
    parent = CognitiveGenome(name="parent")
    child = apply_mutations(
        parent, [Mutation(path="rlm.max_iters", value=12, rationale="test")], name="child"
    )
    assert child.parent == parent.fingerprint()
    assert child.rlm.max_iters == 12
    assert child.fingerprint() != parent.fingerprint()
