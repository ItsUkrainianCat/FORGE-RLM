# FORGE v4 + AIDE — Claude Code project instructions

FORGE is an evidence-driven cognitive foundry for local/open language models. The initial target is a Qwen-class ~27B checkpoint. FORGE v4 adds a controlled self-evolving AI R&D subsystem under `forge/aide/`.

## Mission

Improve **measured research capability and research efficiency**, not rhetoric. The system may optimize its harness, routing, prompts, context management, verification, memory, tool policy, test-time compute, and later produce distillation data. Every accepted change must survive reproducible evaluation.

## Non-negotiable research rules

1. **Measure before modifying.** Preserve `RAW_QWEN`, `DSPY_DIRECT`, and `BEST_KNOWN`.
2. **Never optimize on sealed holdout answers.** Private evaluator data is evaluator-only.
3. **Separate public optimization signal from private selection signal.** The AIDE inner loop may see public task feedback; the outer loop sees only aggregate private grades/decisions.
4. **Fixed budget means fixed budget.** A candidate that wins only by spending more compute is not a research-efficiency improvement.
5. **No one-run promotions.** Use repeated seeds and noise-aware paired comparisons.
6. **External generalization matters.** Selection-benchmark gains alone do not establish transferable improvement.
7. **Reward-hacking/proxy exploitation is a first-class failure mode.** Evaluate proxy gains against downstream outcomes.
8. **Do not rewrite evaluation code to make a candidate pass.** Evaluator repairs are separate reviewed infrastructure changes.
9. **Autonomous self-modification is harness-scoped.** Protected paths, permissions, holdouts, governance, hooks, and pause controls are outside the mutation surface.
10. **No self-granted permissions.** Capability improvements never imply more filesystem/network/secret/deployment access.
11. **Ignition is gated.** A self-improved agent may drive the next outer loop only after the ignition protocol and explicit human approval.
12. **Progression gates can pause the run.** Do not bypass `.forge/PAUSED`; clearing it requires explicit approval.
13. **Correctness, generalization, calibration, provenance, and control outrank persona/style.**
14. **Do not claim AGI/ASI/global SOTA.** Use `project-SOTA`, `best-known`, and measured deltas.
15. **Complexity must earn itself.** Every new agent/tool/memory layer/recursion step needs an ablation path.
16. **Preserve unrelated user work.** Inspect Git status before edits and checkpoint before structural changes.
17. **Current APIs win.** Verify installed DSPy/GEPA/Ruflo/RuVector/RVF/Claude Code surfaces rather than guessing.

## Required reading before autonomous R&D work

- `docs/ARCHITECTURE.md`
- `docs/AIDE_RSI_DESIGN.md`
- `docs/AIDE_EVAL_SECURITY.md`
- `docs/AIDE_IGNITION_TEST.md`
- `docs/INTELLIGENCE_ACCELERATION_GOVERNANCE.md`
- `docs/EXPERIMENT_PROTOCOL.md`
- `docs/EVAL_SPEC.md`
- `docs/SOTA_GATE.md`
- `docs/SECURITY_BOUNDARIES.md`

## Architecture map

- `forge/aide/` — controlled bi-level self-improving AI R&D engine
- `forge/genome/` — reproducible `CognitiveGenome` configurations and lineage
- `forge/controller/` — bottleneck selection, experiment planning, promotion gates
- `forge/runtime/` — routed cognitive runtime
- `forge/rlm/` — DSPy RLM wrapper
- `forge/evaluation/` — grader registry, statistics, reports, sealed holdout boundary
- `forge/optimization/` — GEPA and optimizer tournaments
- `forge/memory/` — provenance-aware memory, epistemic graph, RuVector/RVF adapters
- `forge/curriculum/` — failure clustering and hard-example generation
- `forge/distillation/` — trajectory filtering/export; no automatic training
- `forge/tools/` — permissioned runtime tool registry
- `forge/security/` — trust/provenance boundaries
- `docs/` — protocols, decisions, source notes, results

## AIDE working sequence

For a self-improvement experiment:

1. Confirm the project is not paused: `forge aide status`.
2. Read the AIDE design/eval-security docs.
3. Define a measurable failure cluster and fixed candidate budget.
4. Snapshot/fingerprint the incumbent CognitiveGenome.
5. Run the inner optimizer on public tasks if the experiment requires it.
6. Have the outer research proposer produce **one minimal falsifiable mutation**.
7. Validate mutation scope before applying it in an isolated candidate workspace.
8. Run unit + regression + public/dev evaluation.
9. If qualified, let the evaluator authority run private repeated-seed grading.
10. Apply reward-hacking and external-generalization gates.
11. Promote or revert. Never edit BEST_KNOWN in place.
12. Record lineage, budget, metrics, uncertainty, failures, and lesson.
13. If a candidate is proposed as the new outer-loop driver, run ignition separately.
14. If capability-acceleration governance pauses the run, stop and request human review.

## Claude Code usage

Use Plan Mode before structural changes. Use project Skills rather than expanding this file. Use isolated subagents for independent evaluation. Use hooks for deterministic checks. Use MCP/Ruflo only when the integration adds measured value.

Do not use `/loop` as an unbounded self-improvement mechanism. A recurring loop must have a fixed scope, budget, stop condition, and pause path.

## Core commands

- `make doctor`
- `make test`
- `make lint`
- `make eval-fast`
- `make eval-dev`
- `make aide-validate`
- `make aide-dry-run`
- `uv run forge aide status`
- `uv run forge aide validate`
- `uv run forge aide dry-run`
- `uv run forge genome show config/genome.yaml`

## Definition of a valid improvement

A valid improvement is one that, under comparable budget, improves a defined capability or research-efficiency metric; survives regression checks and repeated evaluation; does not introduce critical safety/provenance failures; and generalizes beyond the exact signal used to select it.

A high score is evidence. It is not permission.
