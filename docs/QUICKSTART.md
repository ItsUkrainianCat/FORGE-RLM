# Quickstart

1. Install Python 3.12 + `uv`, Node 20+, Deno, Claude Code, and your preferred local inference server.
2. `cp .env.example .env` and point it at the OpenAI-compatible Qwen endpoint.
3. `uv sync --all-extras`
4. `bash scripts/doctor_versions.sh`
5. `python scripts/probe_endpoint.py`
6. `make test`
7. `uv run forge genome show config/genome.yaml`
8. `uv run forge run "What is 2+2?"`

Do not enable memory or complex orchestration until RAW_QWEN and DSPY_DIRECT baselines exist.

Inside Claude Code, use `docs/BOOTSTRAP_PROMPT.md` as the first task and then the project Skills under `.claude/skills/`.
