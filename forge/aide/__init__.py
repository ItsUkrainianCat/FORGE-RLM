"""AIDE-inspired recursive AI R&D engine for FORGE.

This package implements a controlled bi-level research loop inspired by published
recursive self-improvement work. It is intentionally separated from evaluation
secrets, host permissions, and production deployment.
"""

from forge.aide.engine import AIDEEngine, AIDERunResult
from forge.aide.schema import AIDEConfig, ResearchBudget

__all__ = ["AIDEEngine", "AIDERunResult", "AIDEConfig", "ResearchBudget"]
