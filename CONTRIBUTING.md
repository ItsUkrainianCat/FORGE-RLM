# Contributing

Start with a small issue describing a bug, reproducibility problem, or falsifiable research hypothesis. Keep changes focused, document assumptions, and avoid replacing architecture without evidence.

## Development

Use Python 3.12 or 3.13 and run from the repository root:

```bash
uv sync --frozen --extra dev --python 3.12
uv run --frozen pytest
uv run --frozen ruff check forge tests scripts
uv run --frozen ruff format --check forge tests scripts
uv run --frozen forge aide validate
uv run --frozen forge aide dry-run --steps 5
```

CI checks offline behavior on both Python versions. Live inference is not part of CI and requires separate credentials and cost authorization. If changing dependencies, regenerate `uv.lock` with a reviewed cutoff and commit both manifest and lockfile. Run `uv build` to check packaging.

## Pull requests

Explain the trigger, resulting behavior, validation performed, and known limitations. Add meaningful tests for behavioral changes. Include evidence for research claims: dataset/model versions, seeds, budget, candidate lineage, uncertainty and failures. Label unexecuted integrations UNVERIFIED. Never present toy results as capability improvements.

Do not include keys, private traces, holdouts, or data without redistribution rights. Report vulnerabilities through SECURITY.md. Changes to governance, evaluation authority, permissions, and promotion policy need explicit maintainer review and must not be applied by an autonomous mutation worker.

Contributions are provided under the repository's MIT license. Follow CODE_OF_CONDUCT.md.
