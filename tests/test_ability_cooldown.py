import pytest

import ability_cooldown as ac

ABILITIES = {
    "fireball": {"cooldown": 2.0, "charges": 2},
    "dash": {"cooldown": 5.0, "charges": 1, "haste": 0.5},
}


def tracker():
    return ac.CooldownTracker({k: dict(v) for k, v in ABILITIES.items()})


def test_initial_charge_is_ready():
    assert tracker().ready("fireball", 0) is True


def test_cast_consumes_one_charge():
    game = tracker()
    game.cast("fireball", 0)
    assert game.state()["abilities"]["fireball"]["charges"] == 1


def test_cast_consumes_last_charge():
    game = tracker()
    game.cast("fireball", 0)
    game.cast("fireball", 0)
    assert game.state()["abilities"]["fireball"]["charges"] == 0


def test_cast_without_charge_raises():
    game = tracker()
    game.cast("fireball", 0)
    game.cast("fireball", 0)
    with pytest.raises(ValueError):
        game.cast("fireball", 0)


def test_partial_recharge_stays_empty():
    game = tracker()
    game.cast("fireball", 0)
    game.cast("fireball", 0)
    game.advance(1.0)
    assert game.state()["abilities"]["fireball"]["charges"] == 0


def test_full_cooldown_restores_one_charge():
    game = tracker()
    game.cast("fireball", 0)
    game.cast("fireball", 0)
    game.advance(2.0)
    assert game.state()["abilities"]["fireball"]["charges"] == 1


def test_two_cooldowns_restore_two_charges():
    game = tracker()
    game.cast("fireball", 0)
    game.cast("fireball", 0)
    game.advance(4.0)
    assert game.state()["abilities"]["fireball"]["charges"] == 2


def test_haste_shortens_recharge():
    game = tracker()
    game.cast("dash", 0)
    game.advance(2.4)
    assert game.state()["abilities"]["dash"]["charges"] == 0
    game.advance(2.5)
    assert game.state()["abilities"]["dash"]["charges"] == 1


def test_progress_tracks_partial_recharge():
    game = tracker()
    game.cast("fireball", 0)
    game.advance(1.0)
    assert game.state()["abilities"]["fireball"]["progress"] == pytest.approx(1.0)


def test_time_travel_raises():
    game = tracker()
    game.advance(5.0)
    with pytest.raises(ValueError):
        game.advance(4.0)


def test_unknown_ability_raises():
    with pytest.raises(ValueError):
        tracker().cast("meteor", 0)


def test_invalid_cooldown_raises():
    with pytest.raises(ValueError):
        ac.CooldownTracker({"bad": {"cooldown": 0, "charges": 1}})


def test_invalid_charge_count_raises():
    with pytest.raises(ValueError):
        ac.CooldownTracker({"bad": {"cooldown": 1, "charges": 0}})


def test_state_returns_a_copy():
    game = tracker()
    snapshot = game.state()
    snapshot["abilities"]["fireball"]["charges"] = 99
    assert game.state()["abilities"]["fireball"]["charges"] == 2


def test_abilities_recharge_independently():
    game = tracker()
    game.cast("fireball", 0)
    game.cast("dash", 0)
    game.advance(2.0)
    assert game.state()["abilities"]["fireball"]["charges"] == 1
    assert game.state()["abilities"]["dash"]["charges"] == 0
