# CognitiveGenome

`CognitiveGenome` is the complete reproducible configuration of one FORGE cognitive architecture candidate.

It contains genes for:

- model/checkpoint and quantization
- decoding
- router thresholds/policies
- RLM budget
- verification stack
- memory backend/policy
- tool router/permissions
- DSPy/GEPA program identity
- optional persona layer

The canonical serialized representation is hashed to produce a fingerprint. Experiments reference fingerprints rather than informal labels.

FORGE initially uses explicit, hypothesis-driven mutations. Do **not** begin with genetic algorithms. Automated search can be added only after evaluation reliability is proven.
