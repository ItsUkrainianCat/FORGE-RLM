---
name: forge-aide-resume
description: Prepare a paused AIDE run for explicit human-reviewed resumption.
allowed-tools: Read, Grep, Glob, Bash
---
# forge-aide-resume

Do not clear the pause yourself. Produce a resumption packet: pause reason, affected experiment, last approved incumbent, unresolved incidents, permission/mutation-scope changes, evaluator integrity, proposed corrective action, and exact command/API a human would use to clear the pause. Resume only after explicit approval outside this skill.
