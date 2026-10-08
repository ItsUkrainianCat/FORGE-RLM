---
name: forge-optimize
description: Run one evidence-driven capability optimization cycle and accept/revert the candidate.
allowed-tools: Read, Grep, Glob, Bash, Write, Edit
---
# forge-optimize

Read `docs/EXPERIMENT_PROTOCOL.md`, `docs/FAILURE_TAXONOMY.md`, `docs/SOTA_GATE.md`, current BEST_KNOWN, and recent experiment records.

1. Identify the highest-value failure cluster.
2. State a falsifiable hypothesis.
3. Fingerprint/checkpoint the parent CognitiveGenome.
4. Make the smallest responsible mutation.
5. Run unit + targeted regression + dev eval.
6. Ask an independent evaluator/critic where subjective.
7. Run adversarial tests if routing/memory/tools/trust changed.
8. Run sealed holdout only if promotion preconditions pass.
9. Promote or revert.
10. Record experiment, lineage, cost, and lesson.

At plateau, stop adding prompt text and diagnose architecture.
