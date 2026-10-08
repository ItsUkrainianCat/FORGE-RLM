# PROJECT-SOTA gate

PROJECT-SOTA means the best measured FORGE configuration discovered under this repository's benchmark and constraints. It does not imply global SOTA, AGI, or ASI.

A candidate may replace `BEST_KNOWN` only if:

1. targeted tests pass;
2. no critical regression is present;
3. dev improvement exceeds the configured minimum or establishes a meaningful Pareto improvement;
4. provenance violations remain zero;
5. catastrophic failures remain zero on gating suites;
6. compute/latency stays inside configured constraints or the quality gain justifies a documented Pareto tradeoff;
7. sealed holdout confirms the improvement;
8. the result survives a second confirmation run for major milestones.

Track at least:

- correctness
- reasoning/task completion
- context resolution
- abstraction switching
- tool accuracy
- retrieval usefulness
- verifier accuracy
- calibration
- self-correction
- long-context performance
- synthesis
- repetition
- hallucination
- catastrophic failures
- p95 latency
- token/subcall cost

Never hide a failed critical case behind a higher average.

## AIDE self-improvement gates

For a harness mutation produced by the self-evolving R&D loop, promotion additionally requires:

- fixed/equivalent candidate research budget;
- repeated seeds sufficient for the configured uncertainty gate;
- a noise-aware paired improvement whose lower confidence bound clears the configured threshold;
- no increase in gated reward-hacking/proxy-exploitation rate;
- no mutation-scope or provenance violations;
- external generalization for major promotions;
- evaluator integrity checks;
- recorded candidate lineage and patch manifest.

A self-improved agent becoming the next **outer-loop improver** is a separate promotion class and requires the ignition protocol plus explicit human approval by default.

## Research-efficiency frontier

FORGE should maintain separate Pareto points such as `FAST_GOOD`, `BEST_BALANCED`, and `MAX_QUALITY`. A configuration is not automatically superior if its quality gain is purchased by disproportionate model calls, latency, or compute.
