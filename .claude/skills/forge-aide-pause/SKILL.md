---
name: forge-aide-pause
description: Pause autonomous AIDE research and preserve enough state for later forensic review.
allowed-tools: Read, Grep, Glob, Bash, Write
---
# forge-aide-pause

Create the configured pause sentinel with a concise reason. Stop new outer-loop mutations. Preserve current incumbent, candidate records, traces, budget/telemetry, Git state, and incidents. Do not delete evidence or auto-resume.
