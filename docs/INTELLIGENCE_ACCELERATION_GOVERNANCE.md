# Capability-acceleration governance

FORGE is designed to automate portions of AI R&D. That creates a second optimization target beyond raw capability: **maintain visibility and control over the rate and scope of automation.**

This document adapts the relevant engineering implications from the September 2026 working paper *What if automating AI R&D triggers an intelligence explosion?* The paper describes a software feedback loop in which better AI R&D systems create better successors and highlights compute, data, hard-to-automate tasks, and time-intensive processes as potential frictions. It also emphasizes visibility, monitoring, pacing, isolation, and incident-response preparation.

FORGE turns those concerns into local engineering controls rather than making a claim that an intelligence explosion is occurring.

## Required telemetry

Every autonomous R&D run should record:

- fraction of research steps executed autonomously;
- accepted harness rewrites;
- candidate evaluation count;
- capability-score delta;
- capability gain per hour;
- capability gain per compute/cost unit;
- time-to-next-incumbent;
- tool/network permission changes (normally zero);
- external generalization results;
- reward-hacking rate;
- incident count;
- failed containment/policy checks.

## Friction ledger

Track whether progress is currently bottlenecked by:

- compute;
- data/evaluation examples;
- tasks that remain hard to automate;
- long-running experiments/training;
- human approval;
- noisy metrics;
- model capability ceiling.

An R&D controller should allocate effort toward the actual bottleneck rather than simply spawning more agents.

## Progression gates

`CapabilityAccelerationMonitor` can pause a run when configured thresholds are crossed. Defaults are intentionally conservative and must be tuned from evidence.

A pause requires explicit human approval to clear. The model cannot edit its own pause policy or permission boundaries through the autonomous mutation surface.

## Isolation

Candidate self-modifications should execute in isolated worktrees/containers with network disabled by default. Sealed holdout data should be accessible only through an evaluator interface returning scores, not raw examples.

## Scope expansion

Increasing any of the following requires a separate reviewed change:

- network access;
- filesystem scope;
- secrets;
- shell privilege;
- allowed mutation paths;
- outer-loop autonomy;
- weight-training automation;
- deployment access.

A capability improvement does not imply a permission improvement.
