from forge.aide.inner_loop import InnerLoopResearchAgent
from forge.aide.schema import AIDEConfig, CandidateProposal, PublicEvaluation, ResearchBudget


def test_inner_loop_runs_bounded_tree_search():
    scores = {"root": 0.0}
    counter = {"n": 0}

    def propose(parent, arm, operator, context):
        counter["n"] += 1
        artifact = f"artifact-{counter['n']}"
        scores[artifact] = (parent.public_score or 0.0) + 0.01
        return CandidateProposal(
            artifact_ref=artifact,
            summary="A sufficiently descriptive synthetic research candidate for testing search behavior.",
            model_calls=1,
            cost_units=1.0,
        )

    def evaluate(artifact):
        return PublicEvaluation(score=scores.get(artifact, 0.0))

    cfg = AIDEConfig(fork_every_steps=2, recent_context_nodes=2)
    result = InnerLoopResearchAgent(cfg, seed=1).run(
        root_artifact_ref="root",
        proposal_fn=propose,
        public_evaluator=evaluate,
        budget=ResearchBudget(max_steps=4, max_model_calls=4, max_cost_units=4, max_wall_time_s=30),
    )
    assert result.budget_usage["steps"] == 4
    assert result.best.public_score is not None
    assert result.best.public_score > 0
    assert len(result.archive.all()) == 5
