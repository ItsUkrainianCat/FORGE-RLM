# Self-evolving AI R&D architecture

FORGE v4 separates self-improvement by timescale.

## Fast: inference-time cognition

Seconds to minutes:

- routing;
- RLM decomposition;
- memory retrieval;
- tools;
- candidate generation;
- verification;
- adaptive test-time compute.

## Medium: harness evolution

Minutes to days:

- AIDE inner/outer loops;
- GEPA/DSPy optimization;
- search-policy changes;
- context-management changes;
- verifier/memory/tool-policy experiments;
- curriculum mining;
- CognitiveGenome mutation and promotion.

This is the primary self-evolving R&D layer.

## Slow: weight evolution

Days to weeks:

- collect high-quality, provenance-backed trajectories;
- rejection filter;
- SFT/distillation;
- optionally investigate verifiable-reward post-training;
- create a new versioned checkpoint;
- rerun naked baseline;
- place the new checkpoint back inside the same harness;
- repeat.

Weight evolution does not occur automatically in v4. `forge/distillation/` prepares artifacts; a training run is a distinct approved experiment.

## Generational loop

```text
MODEL v0
  -> FORGE runtime
  -> AIDE harness RSI
  -> BEST_KNOWN scaffold
  -> validated trajectories
  -> distillation dataset
  -> MODEL v1
  -> naked re-evaluation
  -> same scaffold re-evaluation
  -> new AIDE generation
```

This lets us answer a critical question: did intelligence move into the weights, or is performance still scaffold-dependent?
