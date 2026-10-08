# AIDE quickstart

1. Establish `RAW_QWEN` and `DSPY_DIRECT` baselines first.
2. Run unit tests and `forge aide validate`.
3. Configure public train/dev task families and keep private selection/holdout data sealed.
4. Start with the AIDE engine in dry-run or human-reviewed proposal mode.
5. Run fixed-budget candidate comparisons.
6. Only invoke private grading through the evaluator authority.
7. Promote a harness mutation only after repeated-seed/noise-aware gates pass.
8. Require external generalization and reward-hacking checks before project-SOTA promotion.
9. Run ignition only after the self-improved agent has a stable advantage as an inner research agent.
10. Do not clear a progression pause without explicit human approval.

Useful commands:

```bash
make doctor
make test
uv run forge aide status
uv run forge aide validate
uv run forge aide dry-run
```

Model-backed AIDE runs are intentionally not auto-started. Claude Code should first wire the proposal/build/private-grade adapters to the actual local model and benchmark environment, then run a small reviewed experiment.
