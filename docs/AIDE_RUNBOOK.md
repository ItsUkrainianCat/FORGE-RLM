# AIDE runbook

## Before a run

- Git working tree understood/checkpointed.
- `RAW_QWEN`, `DSPY_DIRECT`, and current BEST_KNOWN recorded.
- `make test` passes.
- `forge aide validate` passes.
- `.forge/PAUSED` absent.
- public/dev data available.
- private evaluator service/interface verified but private cases not exposed.
- fixed budget and seeds recorded in a `ResearchRunManifest`.
- candidate workspace isolation ready.

## During a run

For each outer step:

1. identify current bottleneck from permitted evidence;
2. propose one mutation;
3. validate path/gene scope;
4. build candidate in isolation;
5. run public/regression checks;
6. private evaluator grades repeated seeds under the same budget;
7. inspect proxy/downstream and generalization gates;
8. use noise-aware promotion;
9. record evaluation receipt and lineage;
10. update capability-acceleration telemetry;
11. stop if paused, budget exhausted, or no useful hypothesis remains.

## After a run

- Preserve every accepted/rejected candidate record.
- Review worst failures, not just incumbent trajectory.
- Run external generalization on milestone candidates.
- Run ablations to identify which accumulated changes actually matter.
- Simplify the incumbent by removing artifacts that do not contribute.
- Update research lessons in durable memory only when evidence is sufficient.

## Ignition

Run ignition as a separate experiment. Do not conflate a good inner optimizer with a good outer self-improver.
