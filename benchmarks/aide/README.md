# AIDE benchmark adapters

The self-improvement loop needs **executable R&D tasks**, not chat prompts.

Each selection task should expose two different interfaces:

1. a public task interface available to the inner research agent;
2. a private scorer available only to the evaluator authority.

Candidate harnesses are graded by how well they optimize a collection of tasks under the same per-task budget.

Recommended initial families:

- harness engineering: optimize a small agent/prompt/runtime component against public dev tasks;
- heuristic algorithm engineering: improve a deterministic solver under public instances, grade on hidden instances;
- ML engineering: improve a small training pipeline using public validation, grade on hidden/private examples.

Start small and cheap. Do not reproduce expensive frontier benchmarks before the evaluation boundary works.

See `forge/aide/task_api.py` and `forge/aide/benchmark.py`.
