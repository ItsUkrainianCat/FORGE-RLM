---
name: forge-genome
description: Inspect, fingerprint, mutate, and compare CognitiveGenome configurations safely.
allowed-tools: Read, Grep, Glob, Bash, Write, Edit
---
# forge-genome

Use `forge/genome/`. Never edit BEST_KNOWN in place. Load parent genome, define explicit mutations with rationale, create a child, fingerprint it, and link lineage. Reject unknown mutation paths rather than silently creating config fields.
