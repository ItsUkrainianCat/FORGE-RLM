#!/usr/bin/env bash
set -u
printf '=== FORGE environment audit ===\n'
printf 'python: '; python --version 2>/dev/null || true
printf 'uv: '; uv --version 2>/dev/null || true
printf 'node: '; node --version 2>/dev/null || true
printf 'npm: '; npm --version 2>/dev/null || true
printf 'deno: '; deno --version 2>/dev/null | head -1 || true
printf 'git: '; git --version 2>/dev/null || true
printf 'claude: '; claude --version 2>/dev/null || true
printf 'ruflo: '; npx ruflo@latest --version 2>/dev/null || true
printf 'ruvector: '; npx ruvector --version 2>/dev/null || true
python -c "import dspy; print('dspy:', getattr(dspy,'__version__','unknown')); print('dspy.RLM:', hasattr(dspy,'RLM')); print('dspy.GEPA:', hasattr(dspy,'GEPA'))" 2>/dev/null || true
