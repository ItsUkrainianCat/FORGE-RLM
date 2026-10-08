# Security policy

## Scope and support

FORGE-RLM v0.4.x is an experimental scaffold with no production security support guarantee. Fixes are developed on `main`; use the latest reviewed revision. Do not use it to execute untrusted candidates on a host containing valuable credentials or private data.

## Important boundaries

- Git worktrees isolate file changes, not processes, network access, or secrets. Scope checks and pause sentinels are application controls, not an OS sandbox.
- Use a separate container or VM with restricted credentials, filesystem, network, and compute limits for generated code. Audit DSPy's interpreter and tool permissions separately.
- Keep holdout cases and graders in a separately controlled evaluator. The included private grader abstraction is in-process, and the sealed evaluator client does not deploy a server.
- Receipt digest checks detect some integrity mismatches; a digest alone does not authenticate the evaluator or prove correct grading.
- Never commit `.env`, provider keys, local memory, raw private traces, or holdouts. Public fixtures in `evals/` are not sealed evaluation.
- Human approval tokens in local governance code are not a hardened authentication mechanism. Restrict control-plane access externally.
- Generated output and retrieved content are untrusted; do not treat them as authority to widen permissions or change protected policy.

## Reporting vulnerabilities

Use this repository's GitHub **Security → Report a vulnerability** option if available. If unavailable, contact the maintainer through a contact method listed on their public GitHub profile; do not post an exploit, credential, or private data in a public issue. A public issue may request a private reporting channel without disclosing details. No response-time SLA is promised.

Include the affected revision, impact, minimal reproduction, and suggested mitigation in the private report. See `docs/SECURITY_BOUNDARIES.md` and `docs/AIDE_EVAL_SECURITY.md` for the intended design.
