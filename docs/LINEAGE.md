# Lineage

Record each derived runtime or checkpoint:

```text
QWEN_BASE
  └─ FORGE runtime v1
      └─ GEPA program v2
          └─ filtered trajectories dataset v1
              └─ future distilled QWEN child
```

For each child: parent hash, data provenance, optimizer/training recipe, eval commit, known limitations.
