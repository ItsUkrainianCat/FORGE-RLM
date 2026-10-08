# AIDE evaluation security and anti-gaming design

Recursive optimization will exploit whatever signal is easiest to improve. Evaluation design is therefore part of the security boundary.

## Separation of signals

- Inner loop: public task score and execution feedback.
- Outer loop: sealed private grade.
- External generalization: benchmarks not used for candidate selection.
- Reward-hacking checks: proxy outcome compared with downstream outcome.

## Protected artifacts

Autonomous mutations cannot access or modify:

- `evals/holdout/` or `.forge/holdout/`;
- hidden expected outputs;
- private grader code;
- holdout access controls;
- progression/pause enforcement;
- security/tool permission configuration.

## Evaluator bugs

If a candidate discovers an evaluator defect, classify it as an **evaluation incident**. Do not count exploiting the defect as an improvement. Repairing evaluator infrastructure is a separate reviewed patch, followed by baseline re-evaluation when necessary.

## Noise

Nested loops multiply evaluation noise. Promotion uses repeated seeds, paired comparisons, confidence intervals, catastrophic-failure gates, and cost parity. Results that are inconclusive remain inconclusive.

## Benchmark changes

Changing the benchmark is a new benchmark version. Never rewrite a metric merely because the incumbent failed it.
