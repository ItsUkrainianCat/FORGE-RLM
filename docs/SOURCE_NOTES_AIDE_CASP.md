# Source notes: AIDE RSI + automated AI R&D acceleration

This repository was extended using two user-provided September 2026 sources.

## Weco AI — *Recursive self-improvement of AI research agents*

Design ideas incorporated as hypotheses/components:

- bi-level inner/outer optimization;
- outer selection based on private held-out grades;
- fixed per-task budgets;
- tree search over research artifacts;
- draft/debug/improve-style operators;
- strategy diversity through bandit allocation;
- periodic forking of the current champion to escape plateaus;
- bounded context instead of unbounded history concatenation;
- bug-rate-gated recurring failure memory;
- explicit defenses against untrustworthy/lucky wins;
- evaluation of proxy-vs-downstream reward hacking;
- external held-out generalization;
- an "ignition" test before a self-improved agent is promoted to drive the outer loop;
- explicit recognition that noise and cost limit conclusions.

FORGE extends these with statistical promotion gates, immutable CognitiveGenome lineage, protected mutation surfaces, a capability-acceleration monitor, and explicit pause/approval controls.

## Chan et al. — *What if automating AI R&D triggers an intelligence explosion?*

Engineering implications incorporated:

- model automated R&D as a feedback loop, not a single inference improvement;
- track compute, data, hard-to-automate work, and time-intensive experiments as frictions;
- monitor automation/capability acceleration rather than assuming it;
- preserve visibility and auditability;
- provide progression/pacing gates;
- isolate higher-risk autonomous R&D workloads;
- maintain incident-response and pause capability;
- do not let faster capability growth outrun oversight.

The repository does not assert that its local model is AGI/ASI or that an intelligence explosion is occurring.
