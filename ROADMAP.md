# Research roadmap

This roadmap describes proposed work, not measured achievements or promised dates.

## Publication baseline — v0.4.0

- Preserve the supplied v4 code, public fixtures, configs, prompts and design assets.
- Provide locked setup, offline tests/lint CI, and honest integration status.
- Publish architecture, contribution and security guidance plus a Featherless pilot plan.

## Next: validate the live runtime

- Audit one available model endpoint; record raw-model and DSPy-direct baselines.
- Verify RLM interpreter compatibility and collect sanitized traces.
- Measure verifier errors, tool failures, token use, latency and actual cost.

## Then: controlled harness experiments

- Wire actual budget enforcement and accounting around provider calls.
- Deploy candidate execution in a restricted container/VM, beyond worktree separation.
- Deploy an independently controlled evaluator with authenticated receipts.
- Run equal-budget direct/RLM/verification ablations and repeated-seed evaluation.
- Publish negative and inconclusive results alongside any positive findings.

## Later: automated research and transfer

- Test narrow mutations against fixed development tasks and separate holdouts.
- Validate GEPA and optional memory adapters with real traces and recovery tests.
- Require generalization, anti-gaming checks and governance review before promotion.
- Consider licensed trajectory distillation only after transferable gains are measured.

Completion requires executable evidence and reviewed artifacts. Unit tests alone do not close live research milestones.
