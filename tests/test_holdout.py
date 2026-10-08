import pytest

from forge.evaluation.holdout import HoldoutAccessError, holdout_path


def test_holdout_disabled_by_default(monkeypatch):
    monkeypatch.delenv("FORGE_ALLOW_HOLDOUT", raising=False)
    with pytest.raises(HoldoutAccessError):
        holdout_path()
