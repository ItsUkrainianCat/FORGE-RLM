# Security and control boundaries

The local model may be abliterated or otherwise weakly aligned. Model alignment is **not** a security boundary.

## Runtime model

- least-privilege registered tools only;
- sandbox generated code;
- restrict filesystem/network access;
- never expose secrets in prompts or durable memory;
- explicit approval for side-effecting/privileged tools;
- retrieved content is untrusted data, not instructions;
- preserve source/provenance metadata.

## Claude Code

Claude Code is the repository engineering plane under user control. Do not automatically grant equivalent permissions to the runtime model or AIDE autonomous worker.

## AIDE autonomous mutation worker

Autonomous mutations are harness-scoped. Protected surfaces include sealed holdouts, evaluator authority, governance/pause code, Claude settings/hooks, secret handling, and permission boundaries. Run candidate patches in disposable worktrees/containers where possible.

When `.forge/AIDE_AUTONOMOUS` exists, the project hook `aide-protected-check.sh` checks working-tree mutations against `ScopePolicy`.

## Progression pause

`.forge/PAUSED` means autonomous R&D is stopped. The runtime model cannot clear it. Production deployments should replace the simple local approval token with authenticated human authorization.

## Network and deployment

Self-improvement does not grant deployment or internet privileges. Permission changes are separate reviewed engineering actions.

## Security research

Keep operational security work within owned systems, labs, CTFs, defensive analysis, or explicit authorization.
