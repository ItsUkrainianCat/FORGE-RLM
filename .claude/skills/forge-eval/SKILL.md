---
name: forge-eval
description: Run FORGE evaluation without modifying production cognitive components.
allowed-tools: Read, Grep, Glob, Bash, Write, Edit
---
# forge-eval

Act as evaluator. Validate dataset/grader integrity, run requested split, preserve raw case results, inspect critical/worst failures, and report uncertainty/cost. Do not edit prompts, routing, memory policy, or optimizer state during the evaluation run.
