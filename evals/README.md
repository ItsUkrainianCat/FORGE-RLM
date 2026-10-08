# Evaluation data

Tracked directories contain train/dev/regression/adversarial cases. The **sealed holdout is not stored here**; it belongs under `.forge/holdout/`, which is gitignored and access-gated by `FORGE_ALLOW_HOLDOUT`.

Each JSONL case uses:

- `id`
- `query`
- optional `context`
- `grader`
- `expected`
- `tags`
- `critical`
- optional metadata

Do not place executable code from untrusted datasets into an evaluator. Unit/integration tests should live in trusted test files and be referenced by trusted grader plugins.
