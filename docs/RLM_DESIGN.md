# RLM design

DSPy RLM is used for tasks that benefit from programmatic exploration of large/noisy context and recursive sub-LM analysis. It is not a universal replacement for direct inference.

`forge/rlm/core.py` is the single version-sensitive adapter. The current expected API uses `max_iters`, `max_llm_calls`, `max_output_chars`, `tools`, `sub_lm`, and an interpreter factory/default sandbox.

Track iterations, sub-LM calls, tool calls, answer quality, latency, token usage, repeated subqueries, and verification result. Find the quality/compute elbow experimentally.
