#!/usr/bin/env bash
set -euo pipefail

command -v uv >/dev/null 2>&1 || { echo "Install uv first: https://docs.astral.sh/uv/"; exit 1; }
uv sync --frozen --all-extras

echo "Python dependencies installed."
echo "Next: copy .env.example to .env and configure your local Qwen endpoint."
echo "DSPy RLM default sandbox requires Deno; run 'deno --version' to verify."
