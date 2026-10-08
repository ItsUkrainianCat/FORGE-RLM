# Architecture — FORGE v4 + AIDE

FORGE separates four planes so that capability optimization, evaluation authority, durable memory, and engineering permissions do not collapse into one self-referential process.

## 1. Runtime cognition plane

```text
request
  -> task/difficulty router
  -> compute governor
  -> direct | verify | RLM | memory | tools | multi-candidate
  -> verifier pipeline
  -> answer + trace + calibrated metadata
```

Additional inference compute is conditional, not automatic.

## 2. AIDE research plane

```text
PUBLIC TASKS
   │
   ▼
INNER LOOP
fixed-budget tree search
strategy bandit + champion forking
bounded context + failure memory
   │
   ▼
best task artifacts

            PRIVATE EVALUATION AUTHORITY
                      ▲
                      │ private grade only
                      │
COGNITIVE GENOME -> OUTER LOOP -> candidate harness
                         │
                         ├─ scope validation
                         ├─ isolated build
                         ├─ repeated seeds
                         ├─ reward-hacking checks
                         ├─ external generalization
                         └─ noise-aware promotion
                                      │
                            BEST_KNOWN or revert
                                      │
                                      ▼
                                 IGNITION TEST
                                      │
                              explicit approval
                                      │
                            possible outer-driver promotion
```

The private evaluator and progression-control code are not part of the autonomous mutation surface.

## 3. Durable cognition plane

```text
source -> evidence -> claim -> dependency graph -> action -> outcome
                            |                     |
                            +-- contradiction ----+
```

RuVector/RVF are optional storage/portability substrates. Epistemic/provenance rules belong to FORGE and remain testable independent of backend.

## 4. Engineering/governance plane

Claude Code performs repository engineering. Ruflo may coordinate specialists. The runtime model and AIDE autonomous mutation worker receive narrower capabilities.

```text
telemetry -> acceleration monitor -> continue | PAUSE
                                  -> incident record
                                  -> human review
```

A capability gain never widens permissions automatically.

## Core abstractions

### CognitiveGenome
Reproducible configuration of model, inference, routing, RLM, verification, memory, tools, optimization state, persona, AIDE policy, and governance genes. Unit of architecture experimentation.

### CapabilityGenome
Measured capability vector. Describes performance, not configuration.

### CandidateArchive
Append-only tree of inner-loop task solutions.

### EvaluationAuthority
Private selection boundary. Returns grades; does not expose sealed examples to optimizing agents.

### ImprovementProposal
One falsifiable harness mutation plus an explicit path-level patch manifest.

### IgnitionReport
Evidence about whether a self-improved agent is qualified to drive subsequent recursive improvement.

### PredictionEnvelope
Runtime answer plus route, latency, trace, evidence, and confidence metadata.

## Trust boundaries

Claude Code may edit the repository under user control. Autonomous AIDE runs are harness-scoped and should execute candidate modifications in isolated worktrees/containers. Runtime models receive only registered least-privilege tools. Sealed holdout data and governance controls are separate authority domains.
