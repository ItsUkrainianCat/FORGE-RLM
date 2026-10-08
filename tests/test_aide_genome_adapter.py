import pytest

from forge.aide.genome_adapter import apply_proposal_to_genome
from forge.aide.schema import GenomeMutationSpec, ImprovementProposal, PatchManifest
from forge.genome.schema import CognitiveGenome


def proposal(path: str, value):
    return ImprovementProposal(
        proposal_id="p1",
        parent_genome="parent",
        mutation_label="test",
        target_failure_cluster="routing",
        hypothesis="test mutation",
        expected_effect="test",
        patch=PatchManifest(),
        genome_mutations=[GenomeMutationSpec(path=path, value=value, rationale="test")],
    )


def test_allowed_genome_gene_can_mutate():
    parent = CognitiveGenome(name="g0")
    child = apply_proposal_to_genome(parent, proposal("router.direct_threshold", 0.3))
    assert child.router.direct_threshold == 0.3
    assert child.parent == parent.fingerprint()


def test_permission_and_governance_genes_are_protected():
    parent = CognitiveGenome(name="g0")
    with pytest.raises(PermissionError):
        apply_proposal_to_genome(parent, proposal("tools.allowed_domains", ["everything"]))
    with pytest.raises(PermissionError):
        apply_proposal_to_genome(parent, proposal("governance.progression_gates", False))
