---
name: forge-promote
description: Gate a candidate against BEST_KNOWN and promote only on validated evidence.
allowed-tools: Read, Grep, Glob, Bash, Write, Edit
---
# forge-promote

Check unit/regression/dev, critical failures, provenance, compute constraints, adversarial results, and sealed holdout delta. If any hard gate fails, reject/revert. If the candidate is a Pareto improvement, record exact tradeoff before promotion.
