# AIDE + Ruflo swarm design

Ruflo is optional coordination infrastructure. It should not own grades or silently decide promotions.

## Recommended research team

For expensive outer-loop steps, a small specialist topology can be useful:

```text
research-director
  ├─ aide-outer-loop          proposes one minimal mutation
  ├─ search-policy-researcher explores alternative search mechanism
  ├─ cognitive-architect      checks architecture-level implications
  ├─ adversarial-critic       searches for gaming/regressions
  └─ evaluation-authority     independent read-only evaluator role
```

The evaluator should remain logically independent and should not receive the proposal author's self-justification.

## Parallelism

Parallelize independent candidate hypotheses only when all candidates receive the same budget and evaluation protocol. Avoid spawning multiple agents that duplicate the same reasoning without diversity objectives.

## Shared memory

Ruflo shared memory may contain:

- experiment queue state;
- non-secret public/dev findings;
- candidate metadata;
- task ownership;
- compressed lessons.

It must not contain sealed holdout examples/answers, secrets, private evaluator code, or approval tokens.

## Promotion

Ruflo can coordinate the steps leading to promotion. `EvaluationAuthority`/promotion policy remains the source of the decision. BEST_KNOWN changes should be explicit and logged.
