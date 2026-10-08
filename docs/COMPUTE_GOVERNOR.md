# Adaptive compute governor

The compute governor maps difficulty/risk signals to a budget profile.

Profiles:

- `fast`: direct inference, minimal verification
- `balanced`: direct + targeted verification or shallow RLM
- `deep`: RLM with larger recursive/subcall budget
- `forensic`: competing hypotheses, tools/memory, independent verification

The long-term goal is to learn the expected value of extra computation from outcome data. The baseline implementation is heuristic and intentionally simple.

Track marginal gain per added iteration/subcall. More reasoning tokens are not automatically better.
