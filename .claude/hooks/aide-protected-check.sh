#!/usr/bin/env bash
set -euo pipefail
cd "${CLAUDE_PROJECT_DIR:-.}"
if [[ -f .forge/AIDE_AUTONOMOUS ]]; then
  uv run python scripts/check_aide_protected_paths.py
fi
