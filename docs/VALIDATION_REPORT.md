# Scaffold validation report

This report records checks rerun for public repository preparation on October 7, 2026.
Environment: Python 3.12.14, DSPy 3.4.0, pytest 9.1.1, Ruff 0.16.10;
dependencies resolved in `uv.lock`. No model endpoint was called.

## Passed

- Python syntax/bytecode compilation for `forge/`, `tests/`, and `scripts/`.
- 42 collected unit tests passed.
- Ruff lint and formatting checks passed for 126 Python files.
- Source distribution and wheel built successfully with `uv build`.
- `forge eval --split regression` validated three public fixture cases (no model scoring).
- `.claude/settings.json` parsed as valid JSON.
- `pyproject.toml` parsed as valid TOML.
- `config/aide.yaml` and `config/genome.yaml` parsed as valid YAML.
- `forge aide validate` confirmed protected holdout/governance paths and an allowed harness mutation path.
- `forge aide dry-run` demonstrated an append-only candidate lineage with both accepted and rejected mutations under fixed synthetic cost and repeated-seed promotion.
- CognitiveGenome with AIDE/governance genes loaded and fingerprinted successfully.

The supplied archive's original report included configuration parsing and genome
checks. Those are retained above as assembly provenance; the publication run
independently reran tests, lint, CLI configuration/AIDE checks, dataset validation,
and distribution builds. Synthetic dry-run grades are not model benchmark results.

## Not validated in this environment

These depend on the user's machine and must remain `UNVERIFIED` until Claude Code runs them there:

- actual Qwen checkpoint serving;
- DSPy RLM execution against that endpoint;
- GEPA optimization against real traces;
- Deno/Pyodide runtime compatibility;
- Ruflo/MCP integration;
- RuVector/RVF native integration;
- real Git worktree candidate isolation in the target repository;
- a separate sealed evaluator service;
- GPU throughput/VRAM behavior;
- any real multi-step recursive self-improvement run;
- ignition evidence;
- weight distillation/fine-tuning.

Do not convert these items from `UNVERIFIED` to "working" based on documentation alone. Execute them and record evidence.
