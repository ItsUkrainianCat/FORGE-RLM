# AIDE-inspired recursive AI R&D engine

FORGE v4 adds a controlled bi-level recursive self-improvement (RSI) subsystem under `forge/aide/`.

The design is inspired by the 2026 Weco AI paper *Recursive self-improvement of AI research agents*. It is not a copy of Weco's implementation and must not be described as AIDE2 itself.

## Core idea

There are two different optimization loops.

### Inner loop

The inner research agent receives a task artifact, a public/visible metric, execution feedback, and a fixed budget. It performs tree search over candidate solutions. The inner loop never receives the private outer selection benchmark.

### Outer loop

The outer research agent proposes mutations to the research harness itself. Every candidate harness is evaluated as an optimizer on multiple AI R&D tasks under a fixed budget. A sealed `EvaluationAuthority` computes the private grade. The candidate sees only the resulting decision/aggregate, not the hidden examples.

Accepted harness changes become the next incumbent. Rejected candidates remain in lineage/experiment records but do not replace BEST_KNOWN.

## Search policy

The default inner search uses a portfolio of strategy arms:

- `conservative`
- `aggressive_rewrite`
- `ensemble`
- `tuned_specialist`
- `robust_simple`

`StrategyBandit` uses UCB1 most of the time and configurable softmax exploration over the arms' best observed rewards. Every `fork_every_steps` steps, search deliberately forks the current champion under another strategy. This is designed to escape a plateau without throwing away the strongest artifact already found.

These defaults are source-inspired hypotheses. They are genes. FORGE must ablate and optimize them rather than treating them as universal constants.

## Bounded context and failure memory

Long-run history is not concatenated blindly. `ContextCompactor` supplies the root plus recent candidates. If the observed bug rate crosses a configured threshold, a small deduplicated set of recurring error signatures is also injected.

The point is to keep context approximately bounded while preserving failure information with high expected reuse value.

## Public/private separation

The inner optimizer uses public feedback. Outer selection uses a private grade produced by `EvaluationAuthority`.

This separation is a hard boundary. Autonomous proposal code is forbidden from modifying or reading sealed holdout content or the private grader implementation.

## Fixed budgets

Candidate comparisons are meaningful only under comparable budgets. AIDE configuration therefore tracks steps, model calls, cost units, and wall-clock bounds. Promotion can reject a candidate that improves only because it consumed more research budget.

## Noise-aware promotion

One lucky run must not become the new self-improver. `NoiseAwarePromotionPolicy` requires repeated seeds and uses a paired bootstrap confidence interval over candidate-vs-incumbent deltas. Promotion fails if the lower confidence bound does not clear the configured improvement threshold.

This directly addresses a key failure mode of nested self-improvement: noisy acceptance can corrupt the incumbent and distort every later step.

## Reward-hacking checks

`reward_hacking.py` supports proxy-vs-downstream evaluation. A candidate that improves a visible proxy while failing the downstream objective is counted as a proxy exploitation case. Promotion policy can require no increase in the held-out reward-hacking rate.

## Ignition test

An improved inner research agent is not automatically allowed to become the outer-loop improver. `ignition.py` compares a candidate outer driver against a reference across matched seeds. It reports endpoint quality and time-to-threshold. By default, FORGE also requires explicit human approval before changing the outer-loop driver.

## Mutation surface

Self-modification is harness-scoped. `ScopePolicy` allows research code/prompt/config mutations while protecting:

- sealed holdouts;
- evaluator authority;
- governance/pause mechanisms;
- permission configuration;
- Claude hooks/settings;
- core SOTA/security policy documents.

Changes to protected infrastructure are separate engineering changes, not autonomous AIDE mutations.

## What is allowed to evolve

Typical genes:

- RLM instructions and recursion budget;
- router thresholds/policies;
- verification stack;
- search policy;
- context compaction;
- retrieval/memory policy;
- tool routing;
- candidate count/selection;
- decoding parameters;
- GEPA-optimized DSPy program components.

Later generations may use selected successful traces for distillation. Weight changes are a separate, versioned generation step and must be benchmarked both naked and inside the same scaffold.
