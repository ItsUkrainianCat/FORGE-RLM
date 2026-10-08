# Memory architecture

FORGE separates memory policy from storage backend.

## Logical layer

- episodic
- semantic
- procedural
- experimental
- failure
- evidence
- decision

Each record preserves source, confidence, provenance, status, supersession, outcome, and optional expiry.

## Epistemic layer

Claims can be linked to evidence and other claims via `supports`, `contradicts`, `supersedes`, `derived_from`, `depends_on`, `validated_by`, and `failed_under`.

A retracted premise can invalidate dependent conclusions. Retrieval should eventually answer both **what is relevant?** and **why do we believe it?**

## Backend layer

RuVector is an optional durable semantic/graph backend. RVF is an optional portable artifact. Current APIs are version-sensitive; bind them only after inspecting the installed environment.

Never allow a model-generated hypothesis to be stored, retrieved later, and treated as independent confirmation without external validation.
