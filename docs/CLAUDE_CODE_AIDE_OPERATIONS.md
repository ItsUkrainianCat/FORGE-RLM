# Claude Code operations for AIDE

Claude Code is the engineering control plane, not the autonomous runtime model.

## Project agents

AIDE-specific agents live under `.claude/agents/`:

- `aide-outer-loop`
- `aide-inner-loop`
- `evaluation-authority`
- `ignition-auditor`
- `governance-monitor`
- `search-policy-researcher`
- `research-governor`

Use isolated subagent contexts when independence matters.

## Skills

AIDE-specific reusable workflows:

- `/forge-aide-run`
- `/forge-aide-candidate`
- `/forge-aide-ignition`
- `/forge-aide-audit`
- `/forge-aide-pause`
- `/forge-aide-resume`
- `/forge-rd-govern`

## Hooks

During explicitly armed autonomous mutation mode, `.claude/hooks/aide-protected-check.sh` checks working-tree changes against the mutation scope. The guard is armed by creating `.forge/AIDE_AUTONOMOUS` through `scripts/aide_arm_autonomous.py` with a human acknowledgement.

This hook is defense-in-depth, not a perfect sandbox. Candidate execution should still use isolated worktrees/containers.

## Long runs

Do not create an unbounded `/loop` that continuously rewrites the project. A long research run needs:

- maximum outer steps;
- fixed per-candidate budget;
- run manifest;
- stop conditions;
- pause path;
- BEST_KNOWN rollback;
- evaluator separation;
- periodic human review.

The outer loop should stop when evidence is exhausted, not when the clock says to keep generating mutations.
