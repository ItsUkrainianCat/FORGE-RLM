# Claude Code bootstrap prompt — FORGE v4 + AIDE

Paste this into Claude Code from the repository root:

> Read `CLAUDE.md`, `docs/ARCHITECTURE.md`, `docs/AIDE_RSI_DESIGN.md`, `docs/AIDE_EVAL_SECURITY.md`, `docs/AIDE_IGNITION_TEST.md`, `docs/INTELLIGENCE_ACCELERATION_GOVERNANCE.md`, `docs/EXPERIMENT_PROTOCOL.md`, `docs/EVAL_SPEC.md`, `docs/SOTA_GATE.md`, and `docs/SECURITY_BOUNDARIES.md`.
>
> Inspect Git status and the actual machine. Run `make doctor`, `make test`, `make aide-validate`, and probe the configured Qwen endpoint. Do not start recursive self-improvement yet.
>
> First establish and preserve `RAW_QWEN` and `DSPY_DIRECT` baselines. Verify that the DSPy RLM path works and that train/dev/regression/holdout boundaries are real. Verify installed Ruflo/RuVector/RVF APIs before changing adapters.
>
> Then perform a milestone audit of the AIDE subsystem. The target architecture is a controlled bi-level AI R&D loop: an inner fixed-budget task optimizer using public feedback, and an outer harness improver selected only by a sealed private evaluator authority. Candidate changes must be path-scoped, evaluated in isolation, compared under equal budgets, repeated across seeds, checked for reward hacking and external generalization, and promoted only through noise-aware gates. A self-improved candidate may not become the next outer-loop driver without the ignition protocol and explicit human approval.
>
> Implement missing adapters needed to make one **small end-to-end AIDE experiment** real on the local machine. Do not broaden permissions, expose sealed holdouts, or automate weight training. Use project Skills/subagents for independent roles. Record every change as a falsifiable experiment. If capability-acceleration governance creates `.forge/PAUSED`, stop autonomous R&D and prepare a review packet rather than bypassing it.
>
> The first success criterion is not ASI. It is a reproducible demonstration that, at the same research budget, the AIDE-enhanced harness finds a better solution or better research policy than the baseline and that the gain survives a separate evaluation signal.
