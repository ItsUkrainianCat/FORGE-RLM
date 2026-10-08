#!/usr/bin/env bash
set -u
cd "${CLAUDE_PROJECT_DIR:-$(pwd)}"
# Cheap, non-blocking checks only. Full capability evals are explicit Skills/commands.
python -m compileall -q forge tests scripts >/tmp/forge-compile.log 2>&1 || true
python scripts/validate_eval_integrity.py >/tmp/forge-eval-integrity.log 2>&1 || true
if command -v uv >/dev/null 2>&1 && [ -f pyproject.toml ]; then
  uv run ruff check forge tests scripts >/tmp/forge-ruff.log 2>&1 || true
fi
exit 0
