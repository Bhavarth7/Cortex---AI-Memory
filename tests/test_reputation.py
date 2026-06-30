from cortex.core import reputation as rep


def test_alpha_schedule():
    assert rep.alpha_for(0) == 0.25
    assert rep.alpha_for(9) == 0.25
    assert rep.alpha_for(10) == 0.10
    assert rep.alpha_for(29) == 0.10
    assert rep.alpha_for(30) == 0.05


def test_update_moves_toward_observation():
    r = rep.SkillRep(reputation_score=0.50, observations=0)
    updated = rep.update_reputation(r, observed_score=1.0)
    assert 0.50 < updated.reputation_score < 1.0
    assert updated.observations == 1


def test_confidence_factor_grows_with_history():
    assert rep.confidence_factor(0) == 0.0
    assert rep.confidence_factor(2) < rep.confidence_factor(30)
    assert rep.confidence_factor(30) == 1.0
    assert rep.confidence_factor(100) == 1.0


def test_thin_history_loses_to_deep_history():
    thin = rep.SkillRep(reputation_score=0.90, observations=2)
    deep = rep.SkillRep(reputation_score=0.84, observations=40)
    assert rep.effective_weight(deep) > rep.effective_weight(thin)


def test_combine_observation_weights():
    full = rep.combine_observation(1.0, 0.0, 0.0)
    assert abs(full - 0.50) < 1e-9
    no_human = rep.combine_observation(1.0, 0.0)
    assert abs(no_human - 0.65) < 1e-9
