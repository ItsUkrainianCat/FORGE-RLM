# GEPA design

GEPA is an offline optimizer, not the runtime brain. It may optimize textual/program components such as router, RLM root, verifier, synthesis, and retrieval policies using train/dev traces and rich metric feedback.

Keep the adapter in `forge/optimization/gepa.py` because the API is version-sensitive.

Recommended principles:

- Pareto candidate selection for multi-objective work
- rich textual feedback plus scalar score
- component targeting rather than mutating everything simultaneously
- explicit evaluation/metric budgets
- train/dev only during optimization
- sealed holdout only for final promotion-qualified candidates
- compare GEPA against simpler optimizers/no optimization
