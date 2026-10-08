# Featherless integration and proposed research pilot

## Status

This is a proposed integration and sponsorship plan, not an awarded sponsorship. Live inference against Featherless has not been measured in this publication. No improvement or acceptance rate is promised.

Featherless documents an OpenAI-compatible endpoint at `https://api.featherless.ai/v1`. Check its current [API guide](https://featherless.ai/docs/api-overview-and-common-options), [model catalog](https://featherless.ai/models), and [model API](https://featherless.ai/docs/api-reference-models) for access, supported options, model licenses, pricing, and availability.

## Configuration

1. Complete the offline README checks first.
2. Obtain your own Featherless API key and select an available model ID from the catalog.
3. Edit the ignored `.env` file:

```dotenv
FORGE_API_BASE=https://api.featherless.ai/v1
FORGE_API_KEY=YOUR_FEATHERLESS_API_KEY
# Replace owner/model with an actual catalog ID. Keep the openai/ prefix.
FORGE_MODEL_ID=openai/owner/model
FORGE_SUB_MODEL_ID=openai/owner/model
FORGE_TEMPERATURE=0.2
FORGE_MAX_TOKENS=1024
```

The adapter in `forge/models/openai_compat.py` passes slash-containing model IDs through unchanged. DSPy uses a provider prefix; `openai/owner/model` keeps the OpenAI-compatible provider distinct from the hosted model's owner/name. An unprefixed catalog ID can select the wrong provider.

Run `uv run --frozen forge doctor` to inspect configuration, then a small `forge run` request. Doctor does not test authentication or model availability. A request may incur charges and sends its prompt/context to the provider. Record errors and actual API behavior; do not infer successful integration from configuration alone. RLM and verifier calls can multiply the request count. The local budget objects are not a provider billing limit: set and monitor provider-side limits before experiments.

## Proposed pilot, gated by evidence

| Stage | Work | Reviewable deliverable |
| --- | --- | --- |
| 1 | Confirm endpoint and selected model; establish raw-model and DSPy-direct baselines | Exact model/configuration, dataset revision, raw traces, cost and latency |
| 2 | Compare direct, verification and RLM at equal token/request/time budgets | Ablation table including failures and uncertainty |
| 3 | Search a narrow harness mutation on development tasks | Candidate lineage, immutable budget record, accepted and rejected candidates |
| 4 | Evaluate once on an independently controlled holdout | Repeated-seed report, generalization and anti-gaming checks |
| 5 | Publish findings and reproducibility instructions | Public report, configs, sanitized artifacts and negative results |

The requested support would be inference access or credits sized after baseline measurements, and technical feedback on model compatibility. No arbitrary compute amount or unverified model availability is asserted. Promotion should require an improvement beyond noise under the same budget; inconclusive results remain inconclusive.

## Measurement and publication

Record task accuracy, tool-use failures, token/request counts, billed cost, elapsed time, seed variability, exact model and dataset versions, and candidate fingerprint. Separate development feedback from final evaluation. Do not count synthetic dry-run scores as live results. Release only sanitized, appropriately licensed data; keep API keys and hidden grading assets private.

Weight training or distilled checkpoints are a later research option, conditional on transferable measured gains and model/data licensing. They are not an initial pilot deliverable.
