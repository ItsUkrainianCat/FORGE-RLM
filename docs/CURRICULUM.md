# Curriculum and hard-example mining

FORGE should allocate new examples toward current high-impact failures.

Pipeline:

```text
failed cases -> failure taxonomy -> clusters -> root-cause hypothesis
             -> adversarial/near-boundary task proposals
             -> independent solution/validation
             -> train/dev insertion
```

Never generate new hidden-holdout examples with the same agent that will later inspect their answers. Holdout generation/validation requires an evaluator-owned workflow.
