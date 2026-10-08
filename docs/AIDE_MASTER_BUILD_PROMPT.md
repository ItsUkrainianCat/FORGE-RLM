# Master Claude Code build prompt: operationalize FORGE v4 + AIDE

Use this prompt after the repository has been extracted on the target machine.

---

You are the principal research engineer for FORGE v4. Your job is to make the existing repository operational on this machine, not to redesign it from scratch.

Read `CLAUDE.md` and the AIDE documents first. Inspect all existing code before adding frameworks.

The repository already defines a controlled AIDE-inspired bi-level AI R&D architecture. Preserve these invariants:

- public inner-loop optimization signal and sealed private outer selection signal are separate;
- candidate comparisons use fixed/comparable research budgets;
- promotion uses repeated seeds and uncertainty, not anecdotes;
- reward-hacking/proxy exploitation and external generalization are gated;
- autonomous mutations are harness-scoped;
- holdouts, evaluation authority, permissions, governance, hooks, and pause controls are protected;
- an improved agent cannot become the next outer-loop driver without ignition plus explicit human approval;
- capability gains never grant additional permissions.

## Phase 1 — environment truth

Run doctor/version commands and update `docs/ENVIRONMENT.md`. Verify:

- target Qwen checkpoint and serving backend;
- OpenAI-compatible endpoint;
- DSPy/RLM API;
- GEPA API;
- Deno/Pyodide sandbox;
- Claude Code project agents/Skills/hooks;
- Ruflo mode and MCP if installed;
- RuVector/RVF if installed;
- GPU/VRAM/RAM and practical inference budget.

Do not guess APIs.

## Phase 2 — baselines

Make RAW_QWEN and DSPY_DIRECT genuinely executable. Store reproducible outputs/metrics. Do not touch AIDE until baselines are real.

## Phase 3 — RLM/runtime

Make DIRECT, VERIFY, and RLM routes executable on the local endpoint. Measure quality/latency/calls. Do not assume RLM helps; prove it on appropriate long/noisy-context tasks.

## Phase 4 — private evaluation boundary

Implement the private evaluator as a separate authority boundary. The optimizing agent must be able to submit a candidate and receive an aggregate grade/receipt without reading hidden examples or expected answers. Local-process simulation is acceptable for development; production-quality runs should use a stronger process/container/service boundary.

## Phase 5 — isolated candidate workspaces

Wire ImprovementProposal + PatchManifest into disposable Git worktrees or equivalent isolated candidate directories. Run the mutation-scope check before applying any proposed patch. Network should be disabled by default for autonomous candidate execution unless the experiment explicitly requires and authorizes it.

## Phase 6 — one small end-to-end AIDE experiment

Choose a cheap harness-engineering task. Use a fixed budget. Run:

incumbent -> outer proposal -> isolated candidate -> public/dev evaluation -> repeated-seed private grade -> noise-aware gate -> accept/reject.

Persist the run manifest, candidate lineage, evaluation receipt, costs, and decision.

Do not run dozens of outer steps until one step is trustworthy.

## Phase 7 — search policy

Operationalize inner-loop candidate tree search with strategy arms, UCB1/softmax allocation, champion forking, bounded root/recent context, and bug-rate-gated failure memory. Benchmark against greedy search at exactly the same budget.

Treat every source-inspired constant as a hypothesis. Optimize or remove it based on evidence.

## Phase 8 — GEPA integration

Use GEPA for component-level DSPy optimization where appropriate. Keep AIDE as the meta-level experiment controller. Do not expose sealed holdout data to GEPA. Compare GEPA to simpler/manual or other optimizers on the same target and budget.

## Phase 9 — memory/tools

Only enable RuVector/RVF and additional tools after runtime/eval integrity is established. Measure retrieval and tool-routing accuracy independently. Memory writes require provenance/confidence and must not create self-confirming beliefs.

## Phase 10 — recursive research

After one-step AIDE is trustworthy, run bounded multi-step experiments. Track accepted rewrite velocity, gain/hour, gain/cost, autonomy fraction, evaluator incidents, reward hacking, and external generalization. Honor `.forge/PAUSED` immediately.

## Phase 11 — ignition

Only after a candidate clearly improves inner research efficiency, run a matched-seed ignition experiment comparing it as outer driver against the approved reference. If evidence is inconclusive, HOLD. Do not switch the outer driver automatically.

## Phase 12 — distillation

After scaffold gains are stable, filter only high-quality, provenance-backed successful trajectories into a versioned distillation dataset. Do not launch weight training automatically. A new checkpoint is a new model generation and must be re-baselined naked and inside the same scaffold.

## Research discipline

For every change, record:

PROBLEM
EVIDENCE
HYPOTHESIS
MUTATION
BUDGET
EXPECTED EFFECT
DEV RESULT
PRIVATE RESULT IF QUALIFIED
GENERALIZATION
REWARD-HACKING CHECK
COST/LATENCY
DECISION
LESSON

At plateau, stop adding prompt text. Diagnose architecture, model ceiling, quantization, search, evaluator noise, memory, tools, or the need for weight updates.

Success is a reproducible capability delta under controlled budget, not an impressive architecture diagram.
---
