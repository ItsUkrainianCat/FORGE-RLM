# Research Plan

## Question 1
How much capability can we add to the exact Qwen checkpoint without modifying weights?

## Question 2
Which gains survive when distilled into weights?

## Milestone 1 — Runtime amplification
Raw Qwen → DSPy direct → router → RLM → verifier → memory → GEPA.

## Milestone 2 — Adaptive cognition
Difficulty routing, candidate generation, stronger tool routing, outcome-aware memory, compute/quality frontier.

## Milestone 3 — Distillation
Filter validated traces, rejection sample, SFT/distill, compare naked child model to naked parent and both inside the same scaffold.

## Milestone 4 — Advanced post-training
Only after reward/eval infrastructure is mature: evaluate RLVR/GRPO/GSPO-style methods where rewards are meaningful.
