from forge.aide.schema import PatchManifest, PatchOperation
from forge.aide.scope import ScopePolicy


def test_scope_allows_harness_and_blocks_evaluator_governance():
    p = ScopePolicy()
    assert p.validate_path("forge/routing/router.py")[0]
    assert p.validate_path("prompts/RLM_ROOT.md")[0]
    assert not p.validate_path("evals/holdout/cases.jsonl")[0]
    assert not p.validate_path("forge/aide/governance.py")[0]
    assert not p.validate_path(".claude/settings.json")[0]


def test_manifest_reports_all_violations():
    manifest = PatchManifest(
        operations=[
            PatchOperation(path="forge/routing/router.py", operation="modify", rationale="ok"),
            PatchOperation(path="evals/holdout/x.jsonl", operation="modify", rationale="bad"),
        ]
    )
    ok, problems = ScopePolicy().validate_manifest(manifest)
    assert not ok
    assert any("holdout" in x for x in problems)
