from __future__ import annotations

from pathlib import Path

import typer
from rich import print

from forge.config import Settings
from forge.evaluation.dataset import load_cases
from forge.genome.store import GenomeStore
from forge.routing.router import heuristic_route

app = typer.Typer(no_args_is_help=True)
genome_app = typer.Typer(no_args_is_help=True)
aide_app = typer.Typer(no_args_is_help=True)
app.add_typer(genome_app, name="genome")
app.add_typer(aide_app, name="aide")


@app.command()
def doctor() -> None:
    s = Settings()
    print(
        {
            "model_id": s.model_id,
            "api_base": s.api_base,
            "genome_path": s.genome_path,
            "rvf_path": s.rvf_path,
            "memory_enabled": s.memory_enabled,
            "holdout_enabled": s.allow_holdout,
        }
    )


@app.command()
def route(query: str, context_chars: int = 0) -> None:
    decision = heuristic_route(query, context_chars=context_chars)
    print(
        {
            "route": decision.route.value,
            "compute": decision.compute_profile.value,
            "reason": decision.reason,
        }
    )


@app.command("eval")
def eval_command(split: str = "regression", limit: int | None = None) -> None:
    # Dataset validation command. Model-backed scoring is wired through the runtime after endpoint audit.
    path = Path("evals") / split / "cases.jsonl"
    if not path.exists():
        raise typer.BadParameter(f"missing eval file: {path}")
    rows = load_cases(path)
    if limit:
        rows = rows[:limit]
    graders = sorted({row.grader for row in rows})
    print({"split": split, "cases": len(rows), "graders": graders, "status": "dataset-valid"})


@genome_app.command("show")
def genome_show(path: str = "config/genome.yaml") -> None:
    genome = GenomeStore().load(path)
    print(genome.model_dump(mode="json"))
    print({"fingerprint": genome.fingerprint()})


@genome_app.command("fingerprint")
def genome_fingerprint(path: str = "config/genome.yaml") -> None:
    genome = GenomeStore().load(path)
    print(genome.fingerprint())


@app.command()
def run(query: str, context: str = "") -> None:
    """Run the configured FORGE runtime against the local model endpoint."""
    from forge.runtime.factory import build_runtime

    envelope = build_runtime().predict(query=query, context=context)
    print(envelope.model_dump(mode="json"))


@app.command()
def benchmark() -> None:
    print(
        "Use the configured runtime/evaluator after establishing RAW_QWEN and DSPY_DIRECT baselines."
    )


@aide_app.command("status")
def aide_status() -> None:
    from forge.aide.config import load_aide_config
    from forge.aide.governance import PauseController

    config, policy = load_aide_config()
    pause = PauseController()
    print(
        {
            "enabled": True,
            "paused": pause.is_paused(),
            "pause_reason": pause.reason(),
            "outer_steps": config.outer_steps,
            "strategy_arms": [x.value for x in config.strategy_arms],
            "promotion_confidence": config.promotion_confidence,
            "minimum_seeds": config.minimum_seeds_for_promotion,
            "progression_policy": policy.__dict__,
        }
    )


@aide_app.command("validate")
def aide_validate() -> None:
    from forge.aide.config import load_aide_config
    from forge.aide.scope import ScopePolicy

    config, _ = load_aide_config()
    policy = ScopePolicy()
    checks = {
        "config_valid": True,
        "strategy_arms": [x.value for x in config.strategy_arms],
        "holdout_protected": not policy.validate_path("evals/holdout/cases.jsonl")[0],
        "governance_protected": not policy.validate_path("forge/aide/governance.py")[0],
        "harness_mutation_allowed": policy.validate_path("forge/routing/router.py")[0],
    }
    print(checks)


@aide_app.command("dry-run")
def aide_dry_run(steps: int = 5) -> None:
    from forge.aide.dry_run import run_dry_run

    print(run_dry_run(steps=steps))


@aide_app.command("pause")
def aide_pause(reason: str) -> None:
    from forge.aide.governance import PauseController

    PauseController().pause(reason)
    print({"paused": True, "reason": reason})


@aide_app.command("resume")
def aide_resume(
    approval_token: str = typer.Option(
        ..., help="Explicit human approval token; minimum 8 characters"
    ),
) -> None:
    from forge.aide.governance import PauseController

    PauseController().clear_with_explicit_approval(approval_token)
    print({"paused": False})


if __name__ == "__main__":
    app()
