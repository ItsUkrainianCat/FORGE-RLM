# Evaluator laboratory

The evaluator is the scientific core of FORGE.

Each case declares a grader. Prefer deterministic graders:

- exact match
- normalized contains
- regex
- JSON validity/schema
- label match
- retrieval metrics
- unit/integration tests implemented outside untrusted dataset text

Use LM judges only when deterministic scoring cannot represent the task. Subjective judges should be blind to candidate identity and preferably use pairwise comparison.

Reports must preserve raw prediction, grader feedback, latency, route, trace ID, genome fingerprint, and case metadata.

Promotion should consider paired deltas, confidence intervals where useful, worst-case failures, and compute cost—not only mean score.
