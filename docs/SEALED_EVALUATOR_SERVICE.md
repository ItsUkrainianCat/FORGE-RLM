# Sealed evaluator service

For meaningful outer-loop self-improvement, private selection data should not live in the same authority domain as the optimizing agent.

`forge/aide/evaluator_client.py` defines an aggregate-only client contract:

```text
candidate fingerprint
artifact URI
benchmark version
budget fingerprint
run manifest fingerprint
        |
        v
SEPARATE EVALUATOR
        |
        v
EvaluationReceipt(private aggregate + metadata digest)
```

There is intentionally no API for listing hidden examples, labels, or grader implementation.

A local in-process `EvaluationAuthority` is adequate for unit tests and early development, but it is not a strong secrecy boundary because Python code in the same process can potentially inspect objects. Promotion-quality RSI should isolate the private evaluator in a separate process/container/service with independent credentials and storage.

The evaluator service itself is not included because its hidden data should not be shipped inside the optimizer repository.
