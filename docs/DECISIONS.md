# Decision Log

## D-001 — Python-first cognition
Use Python for DSPy/RLM/GEPA/evals. Introduce Rust only after profiling demonstrates a bottleneck.

## D-002 — Tools external to weights
Models learn when/how to use tools; rapidly changing capabilities remain modular external services.

## D-003 — Memory separated from truth
RuVector/RVF storage is evidence-indexed memory, not an authority. Provenance and validation remain mandatory.

## D-004 — Holdout isolation
Sealed holdout data must not be used by GEPA or prompt-authoring agents.

Add future decisions with alternatives, evidence, tradeoffs, and reversal condition.
