from pathlib import Path

import pytest

from forge.aide.governance import (
    AccelerationSnapshot,
    CapabilityAccelerationMonitor,
    PauseController,
    ProgressionPolicy,
)


def test_acceleration_monitor_triggers_review():
    m = CapabilityAccelerationMonitor(ProgressionPolicy(max_autonomy_fraction_without_review=0.5))
    ok, reasons = m.observe(
        AccelerationSnapshot(
            accepted_rewrites=1,
            evaluated_candidates=3,
            elapsed_hours=2.0,
            incumbent_score=0.72,
            baseline_score=0.70,
            compute_cost_units=10,
            autonomy_fraction=0.8,
        )
    )
    assert not ok
    assert reasons


def test_pause_controller_requires_explicit_token(tmp_path: Path):
    p = PauseController(tmp_path / "PAUSED")
    p.pause("review")
    assert p.is_paused()
    with pytest.raises(PermissionError):
        p.clear_with_explicit_approval("x")
    p.clear_with_explicit_approval("approved-123")
    assert not p.is_paused()
