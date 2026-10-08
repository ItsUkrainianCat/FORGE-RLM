# AIDE + DSPy/GEPA integration

AIDE and GEPA solve different levels of the optimization problem.

## GEPA

GEPA is appropriate for optimizing textual/program components of a DSPy pipeline from traces and evaluator feedback. It can improve prompts/instructions and other optimizable program components without redesigning the whole research process.

## AIDE outer loop

The AIDE outer loop searches a larger harness space. A proposal may choose to:

- run GEPA on one component;
- change which DSPy components exist;
- alter RLM recursion/search policy;
- change router or verifier topology;
- change context compaction;
- change memory/retrieval policy;
- change the optimizer strategy itself;
- reject GEPA entirely for a failure where another method performs better.

Thus:

```text
AIDE outer loop
  -> chooses research mutation
       -> optionally invoke GEPA
       -> build candidate CognitiveGenome/program
       -> fixed-budget task optimization
       -> sealed evaluation
       -> promote/revert
```

Do not let GEPA see sealed holdout examples. Textual optimizer feedback should come from train/dev traces or an evaluation authority that returns permitted aggregate diagnostics.

AIDE should benchmark GEPA against other optimization strategies when the target can be optimized multiple ways. An optimizer does not receive privileged status because it is fashionable.
