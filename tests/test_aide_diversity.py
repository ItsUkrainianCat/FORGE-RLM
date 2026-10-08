from forge.aide.diversity import DiverseCandidate, DiversityArchive


def test_diversity_archive_keeps_best_per_niche():
    a = DiversityArchive()
    assert a.add(DiverseCandidate("x", 0.5, ("simple", "memory-off")))
    assert not a.add(DiverseCandidate("y", 0.4, ("simple", "memory-off")))
    assert a.add(DiverseCandidate("z", 0.6, ("complex", "memory-on")))
    assert a.coverage() == 2
    assert {x.candidate_id for x in a.candidates()} == {"x", "z"}
