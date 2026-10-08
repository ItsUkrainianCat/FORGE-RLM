from __future__ import annotations

from pathlib import Path

import yaml

from forge.aide.governance import ProgressionPolicy
from forge.aide.schema import AIDEConfig


def load_aide_config(path: str | Path = "config/aide.yaml") -> tuple[AIDEConfig, ProgressionPolicy]:
    payload = yaml.safe_load(Path(path).read_text()) or {}
    search = payload.get("search", {})
    context = payload.get("context", {})
    outer = payload.get("outer_loop", {})
    ignition = payload.get("ignition", {})
    governance = payload.get("governance", {})
    config = AIDEConfig(
        strategy_arms=search.get("strategy_arms", None) or AIDEConfig().strategy_arms,
        softmax_exploration_probability=search.get("softmax_exploration_probability", 0.30),
        softmax_temperature=search.get("softmax_temperature", 0.5),
        fork_every_steps=search.get("fork_every_steps", 5),
        recent_context_nodes=context.get("recent_context_nodes", 6),
        failure_memory_bug_rate_threshold=context.get("failure_memory_bug_rate_threshold", 0.15),
        failure_memory_max_signatures=context.get("failure_memory_max_signatures", 3),
        min_candidate_chars=context.get("min_candidate_chars", 40),
        outer_steps=outer.get("steps", 25),
        minimum_seeds_for_promotion=outer.get("minimum_seeds_for_promotion", 3),
        promotion_confidence=outer.get("promotion_confidence", 0.90),
        min_private_delta=outer.get("min_private_delta", 0.0),
        require_fixed_budget=outer.get("fixed_budget", True),
        require_external_generalization=outer.get("require_external_generalization", True),
        require_reward_hacking_check=outer.get("require_reward_hacking_check", True),
        require_human_approval_for_ignition=ignition.get("require_human_approval", True),
    )
    policy = ProgressionPolicy(
        max_autonomy_fraction_without_review=governance.get(
            "max_autonomy_fraction_without_review", 0.80
        ),
        max_accepted_rewrites_without_review=governance.get(
            "max_accepted_rewrites_without_review", 10
        ),
        max_gain_per_hour_without_review=governance.get("max_gain_per_hour_without_review", 0.05),
    )
    return config, policy
