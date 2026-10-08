# Evaluation Specification

## Splits
- train: optimizer-visible examples
- dev: iteration decisions
- holdout: sealed finalist evaluation
- adversarial: unseen stress cases
- regression: historical failures

## Principles
- deterministic graders first
- blind subjective judging where needed
- report mean plus worst cases and failure rate
- preserve raw predictions and config hashes
- no holdout answer exposure to optimization workers

## Core dimensions
Correctness, reasoning, context resolution, abstraction selection, coding/debugging, long-context handling, tool selection, retrieval, calibration, self-correction, repetition control, synthesis, latency, compute.

## Benchmark integrity
If a holdout answer leaks into optimization context, mark the split contaminated and replace it.
