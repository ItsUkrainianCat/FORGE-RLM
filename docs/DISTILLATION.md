# Distillation roadmap

Do not fine-tune until the scaffold demonstrates stable gains.

Later pipeline:

```text
best runtime trajectories
 -> quality/provenance filter
 -> diversity filter
 -> rejection sampling
 -> export training JSONL
 -> SFT/distillation outside the runtime
 -> evaluate naked child checkpoint
 -> evaluate child inside identical scaffold
```

This distinction reveals whether gains moved into weights or remained in the scaffold.

FORGE v3 only selects and exports trajectory data. It does not autonomously launch training.
