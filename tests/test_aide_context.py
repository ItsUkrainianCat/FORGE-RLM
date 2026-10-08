from forge.aide.archive import CandidateArchive
from forge.aide.context import ContextCompactor
from forge.aide.schema import AIDEConfig, CandidateNode, CandidateStatus, OperatorKind, StrategyArm


def node(node_id: str, parent: str | None, *, buggy: bool = False, sig: str | None = None):
    return CandidateNode(
        node_id=node_id,
        parent_id=parent,
        strategy=StrategyArm.CONSERVATIVE,
        operator=OperatorKind.IMPROVE,
        artifact_ref=node_id,
        summary=f"candidate {node_id} with enough descriptive text for the compact context",
        public_score=0.1,
        buggy=buggy,
        error_signature=sig,
        status=CandidateStatus.BUGGY if buggy else CandidateStatus.SCORED,
    )


def test_failure_memory_only_activates_after_bug_threshold():
    root = node("root", None)
    archive = CandidateArchive(root)
    archive.add(node("a", "root", buggy=True, sig="OOM"))
    archive.add(node("b", "a", buggy=False))
    cfg = AIDEConfig(failure_memory_bug_rate_threshold=0.40, failure_memory_max_signatures=3)
    compact = ContextCompactor(cfg).build(archive)
    assert compact.bug_rate == 0.5
    assert compact.failure_signatures == ("OOM",)
    assert "RECURRING FAILURE SIGNATURES" in compact.text


def test_context_is_bounded_to_root_plus_recent():
    root = node("root", None)
    archive = CandidateArchive(root)
    parent = "root"
    for i in range(10):
        nid = f"n{i}"
        archive.add(node(nid, parent))
        parent = nid
    cfg = AIDEConfig(recent_context_nodes=2)
    compact = ContextCompactor(cfg).build(archive)
    assert set(compact.included_node_ids) == {"root", "n8", "n9"}
