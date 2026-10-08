---
name: forge-aide-candidate
description: Design and validate one minimal self-improvement candidate for the FORGE harness.
allowed-tools: Read, Grep, Glob, Bash, Write, Edit
---
# forge-aide-candidate

Start from one measured failure cluster. State hypothesis, expected mechanism, mutation paths, budget, success metric, and likely regressions. Validate the patch manifest against `ScopePolicy`. Implement in an isolated branch/worktree. Run unit/regression/dev before requesting private evaluation. Do not touch protected paths.
