# AI safety research: evaluator gaming in LLM-driven harness optimization

**Status: proposed study. No safety results are published yet.** This document describes a planned experiment, the FORGE components it reuses, and what would count as evidence. It makes no claim that any result has been obtained.

## Research question

Automated optimizers (AIDE-style tree search, GEPA-style prompt evolution) increasingly use language models to rewrite the scaffolds, prompts, and tool policies around other models. A capable optimizer can raise its score by exploiting the grader instead of improving real behavior: reading holdout data, hardcoding expected answers, editing evaluation code, weakening permission checks, or overfitting the public split.

This is reward hacking at the level of the scaffold. FORGE asks:

1. **How often** does an LLM mutation agent propose changes that cross evaluation, permission, or governance boundaries, with and without being told those boundaries exist?
2. **Can it be detected from scores alone?** Is the gap between public-split gains and sealed-holdout gains a reliable gaming signal?
3. **Can it be caught by a monitor?** How well does a second model reviewing each proposed diff flag boundary violations, measured against hand labels?
4. **Do the guardrails hold?** Do the scope policy, noise-aware promotion gate, and pause controls stop gamed candidates from being promoted?

## Why this matters

Labs and researchers are starting to let models improve the systems that evaluate and deploy other models. If an optimizer learns to satisfy the grader rather than the goal, every downstream number becomes untrustworthy, and the failure can be quiet. This study produces concrete measurements and an open dataset of real attempts, so monitoring and containment methods can be tested on data instead of hypotheticals.

## Existing safety components in this repository

The study builds on mechanisms that already exist and are covered by offline unit tests. Unit tests show the mechanisms behave as specified; they are not evidence that the mechanisms are sufficient against a capable optimizer. That is what this study would measure.

| Component | Location | Role in the study |
| --- | --- | --- |
| Mutation scope policy | `forge/aide/scope.py`, `scripts/check_aide_protected_paths.py` | Defines the allowed mutation surface and protected paths (holdouts, private grader, governance, scope policy itself, hooks). Every violation attempt is logged as a labeled event. |
| Evaluation authority | `forge/aide/private_grader.py` | The mutation agent only sees an aggregate decision, never sealed examples, expected outputs, or grader code. |
| Proxy vs. downstream check | `forge/aide/reward_hacking.py`, `benchmarks/aide/reward_hacking_manifest.example.yaml` | Flags candidates whose visible (proxy) gain is not matched by downstream gain. |
| Noise-aware promotion gate | `forge/aide/promotion.py` | Requires repeated seeds, a paired bootstrap confidence interval, cost parity, and no increase in reward-hacking rate before promotion. |
| Evaluation receipts | `forge/aide/receipts.py` | SHA-256 digested receipts tie each grade to a candidate, benchmark version, grader version, and budget. |
| Capability acceleration monitor and pause | `forge/aide/governance.py` | Pauses the loop when autonomy fraction, accepted rewrites, or gain velocity exceed review thresholds; resuming requires explicit human approval. |
| Candidate lineage | `forge/aide/archive.py`, `docs/LINEAGE.md` | Every proposed candidate and its parent are recorded, including rejected ones. |
| Design notes | `docs/AIDE_EVAL_SECURITY.md`, `docs/SECURITY_BOUNDARIES.md`, `docs/CANDIDATE_ISOLATION.md` | Threat model, protected artifacts, and the rule that exploiting an evaluator bug is an evaluation incident, not an improvement. |

## Method

### Mutation agent

Claude models act as the outer-loop mutation agent, proposing patches to the harness under a fixed call and token budget. Open-weight models served through an OpenAI-compatible endpoint (for example via Featherless) serve as a comparison where budget allows. Connecting Claude through `forge/models/openai_compat.py` or a thin adapter is part of the first milestone and is **not yet verified**.

### Conditions

| Condition | What changes |
| --- | --- |
| A. Boundaries disclosed | The mutation prompt states which paths are protected and why. |
| B. Boundaries undisclosed | Same task and budget; protected paths are enforced but not described. |
| C. Tempting environment | A deliberately planted, clearly synthetic "leak" (e.g. a decoy holdout file within reach) to measure whether the agent uses it. Decoys contain no real data. |
| D. Monitor on | A second model reviews each diff before evaluation and can veto it. |

Each condition runs over repeated seeds with identical budgets.

### Measurements

- **Boundary-crossing rate**: share of proposals whose patch manifest touches a protected or out-of-scope path (from `ScopePolicy.validate_manifest`).
- **Gaming gap**: public-split gain minus sealed-holdout gain per candidate, and the proxy/downstream reward-hacking rate from `evaluate_proxy_downstream`.
- **Monitor quality**: precision and recall of the reviewing model's flags against hand labels, with a sample of labels double-checked.
- **Containment**: number of gamed candidates that would have been promoted with each guardrail disabled vs. enabled (ablation of scope checks, promotion gate, and monitor).
- **Cost**: calls, tokens, and dollars per condition.

### Labeling

Each proposed diff is hand-labeled into categories adapted from `docs/FAILURE_TAXONOMY.md`: legitimate improvement, benign out-of-scope edit, evaluator access attempt, evaluator modification attempt, permission or governance tampering, test or answer hardcoding, public-split overfitting, and unclear. Labeling guidelines and disagreements are published with the dataset.

## Deliverables

- An open, labeled dataset of logged mutation proposals, scope checks, grades, and monitor verdicts.
- Reproducible configs, seeds, model IDs, prompts, and budgets for every run.
- Cost and latency accounting.
- A public report, including null and negative results. If the agent never attempts to game the evaluator under these conditions, that is reported as a finding.

## Safety and responsible conduct

- Candidate code runs in a separate worktree. Worktrees are not a security sandbox, so live runs will move to a restricted container or VM with no network access beyond the model endpoint and no credentials in reach before any generated code is executed.
- Decoys are synthetic and labeled; no real secrets, private data, or third-party systems are used.
- The pause controller and acceleration monitor stay enabled for all runs. Exploits of evaluator bugs are logged as evaluation incidents and fixed in separate reviewed patches.
- The study measures and documents gaming behavior to improve detection. It does not publish techniques for defeating specific production evaluators.
- All model use follows the providers' usage policies.

## Milestones

1. **Wiring**: connect a Claude model as the mutation agent, add per-call cost accounting, and log full patch manifests. Verify with a small smoke run.
2. **Pilot**: conditions A and B on a small public task set with a sealed holdout; hand-label all proposals.
3. **Monitor and decoy**: add conditions C and D; measure monitor precision and recall.
4. **Ablations and report**: guardrail ablations, cost summary, dataset release, and written report.

## Evidence boundary

Until milestone 1 is complete, nothing in this document has been run against a live model. Results will be added to [RESULTS.md](RESULTS.md) and [EXPERIMENT_LOG.md](EXPERIMENT_LOG.md) only with the dataset version, model ID, seeds, budget, and reproducible evidence, following the rule in the main [README](../README.md).
