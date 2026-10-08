from forge.aide.bandit import StrategyBandit
from forge.aide.schema import StrategyArm


def test_bandit_tries_every_arm_before_exploitation():
    arms = [StrategyArm.CONSERVATIVE, StrategyArm.AGGRESSIVE_REWRITE, StrategyArm.ENSEMBLE]
    b = StrategyBandit(arms, seed=7)
    chosen = []
    for i in range(len(arms)):
        arm = b.choose()
        chosen.append(arm)
        b.update(arm, float(i))
    assert set(chosen) == set(arms)


def test_bandit_snapshot_is_serializable_shape():
    b = StrategyBandit([StrategyArm.CONSERVATIVE], seed=0)
    arm = b.choose()
    b.update(arm, 0.5)
    snap = b.snapshot()
    assert snap["conservative"]["pulls"] == 1
    assert snap["conservative"]["mean_reward"] == 0.5
