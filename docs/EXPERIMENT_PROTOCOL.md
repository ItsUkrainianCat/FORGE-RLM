# Experiment protocol

Every capability change must be represented as an experiment.

## Required fields

- experiment ID
- parent genome fingerprint
- hypothesis
- mutation(s)
- expected effect
- targeted failure cluster
- train/dev datasets used
- model/inference versions
- result metrics
- latency/token deltas
- regression findings
- holdout result if qualified
- accept/revert decision
- lesson

## Promotion sequence

1. Unit/static checks.
2. Targeted regression cases.
3. Dev evaluation.
4. Independent critic/evaluator when subjective.
5. Adversarial suite if the change touches routing, memory, tools, or trust.
6. Sealed holdout only for candidates that satisfy dev gates.
7. Pareto comparison with `BEST_KNOWN`.
8. Promote or revert.

## Forbidden behavior

- changing expected answers to fit a candidate
- exposing holdout answers to GEPA or prompt-author agents
- promoting on train metrics only
- hiding catastrophic regressions inside average scores
- declaring success from anecdotal examples

## Plateau

If three meaningful iterations fail to improve holdout, stop prompt tuning and perform architectural diagnosis: model ceiling, routing, quantization, retrieval, tool selection, RLM topology, verifier quality, benchmark noise, or need for weight updates.

## AIDE candidate experiments

An AIDE proposal must also record:

- public optimization signal;
- private selection grade version (without exposing hidden cases);
- fixed budget specification;
- search strategy/operator lineage;
- candidate patch manifest;
- repeated-seed private scores;
- proxy/downstream reward-hacking result where applicable;
- external generalization result for promotion-qualified candidates;
- mutation-scope validation;
- acceleration/governance telemetry;
- whether the candidate is being considered for ignition.

### Evaluator incidents

If a candidate exposes a broken grader/evaluator, freeze the affected result. Repair evaluation infrastructure in a separate reviewed experiment and rerun the relevant baselines. Never count evaluator exploitation as a research improvement.

### Self-improvement noise

Because noise compounds across the inner and outer loops, promotion standards should become stricter—not looser—as autonomy increases. A single lucky comparison cannot replace the incumbent.
