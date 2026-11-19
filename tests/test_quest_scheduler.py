import pytest

import quest_scheduler as qs

QUESTS = [
    {"id": "a", "duration": 2, "requires": [], "deadline": 10, "cost": {"gold": 3}, "reward": 5},
    {"id": "b", "duration": 3, "requires": ["a"], "deadline": 10, "cost": {"gold": 2}, "reward": 8},
]


def scheduler(quests=None, slots=2):
    return qs.QuestScheduler(QUESTS if quests is None else quests, slots)


def test_single_quest():
    result = scheduler([QUESTS[0]]).schedule(0, {"gold": 10})
    assert result == [{"id": "a", "slot": 0, "start": 0, "end": 2}]


def test_dependency_order():
    result = scheduler(slots=1).schedule(0, {"gold": 10})
    assert [x["id"] for x in result] == ["a", "b"]
    assert result[1]["start"] == 2


def test_parallel_slots_start_together():
    quests = [
        {"id": "a", "duration": 2, "requires": [], "deadline": 10, "cost": {}, "reward": 0},
        {"id": "b", "duration": 2, "requires": [], "deadline": 10, "cost": {}, "reward": 0},
    ]
    result = scheduler(quests, slots=2).schedule(0, {})
    assert sorted(x["slot"] for x in result) == [0, 1]
    assert all(x["start"] == 0 for x in result)


def test_one_slot_serializes():
    quests = [
        {"id": "a", "duration": 2, "requires": [], "deadline": 10, "cost": {}, "reward": 0},
        {"id": "b", "duration": 2, "requires": [], "deadline": 10, "cost": {}, "reward": 0},
    ]
    result = scheduler(quests, slots=1).schedule(0, {})
    assert [x["start"] for x in result] == [0, 2]


def test_deadline_skip():
    quests = [
        {"id": "late", "duration": 5, "requires": [], "deadline": 3, "cost": {}, "reward": 0},
        {"id": "ok", "duration": 1, "requires": [], "deadline": 3, "cost": {}, "reward": 0},
    ]
    assert [x["id"] for x in scheduler(quests).schedule(0, {})] == ["ok"]


def test_cost_skip():
    quests = [
        {"id": "rich", "duration": 1, "requires": [], "deadline": 10, "cost": {"gold": 5}, "reward": 0},
        {"id": "cheap", "duration": 1, "requires": [], "deadline": 10, "cost": {}, "reward": 0},
    ]
    assert [x["id"] for x in scheduler(quests).schedule(0, {"gold": 1})] == ["cheap"]


def test_reward_enables_next():
    quests = [
        {"id": "a", "duration": 1, "requires": [], "deadline": 10, "cost": {"gold": 5}, "reward": 10},
        {"id": "b", "duration": 1, "requires": [], "deadline": 10, "cost": {"gold": 8}, "reward": 0},
    ]
    assert [x["id"] for x in scheduler(quests, slots=1).schedule(0, {"gold": 5})] == ["a", "b"]


def test_order_deadline_then_id():
    quests = [
        {"id": "b", "duration": 1, "requires": [], "deadline": 5, "cost": {}, "reward": 0},
        {"id": "a", "duration": 1, "requires": [], "deadline": 5, "cost": {}, "reward": 0},
    ]
    assert [x["id"] for x in scheduler(quests, slots=1).schedule(0, {})] == ["a", "b"]


def test_cycle_raises():
    with pytest.raises(ValueError):
        scheduler([
            {"id": "a", "duration": 1, "requires": ["b"], "deadline": 5, "cost": {}, "reward": 0},
            {"id": "b", "duration": 1, "requires": ["a"], "deadline": 5, "cost": {}, "reward": 0},
        ])


def test_missing_dependency_raises():
    with pytest.raises(ValueError):
        scheduler([{"id": "a", "duration": 1, "requires": ["ghost"], "deadline": 5, "cost": {}, "reward": 0}])


def test_duplicate_id_raises():
    with pytest.raises(ValueError):
        scheduler([
            {"id": "a", "duration": 1, "requires": [], "deadline": 5, "cost": {}, "reward": 0},
            {"id": "a", "duration": 2, "requires": [], "deadline": 5, "cost": {}, "reward": 0},
        ])


def test_invalid_duration_raises():
    with pytest.raises(ValueError):
        scheduler([{"id": "a", "duration": 0, "requires": [], "deadline": 5, "cost": {}, "reward": 0}])


def test_schedule_does_not_mutate_resources():
    resources = {"gold": 10}
    result = scheduler().schedule(0, resources)
    assert [x["id"] for x in result] == ["a", "b"]
    assert resources == {"gold": 10}


def test_slot_count_not_exceeded():
    quests = [
        {"id": str(i), "duration": 1, "requires": [], "deadline": 10, "cost": {}, "reward": 0}
        for i in range(5)
    ]
    result = scheduler(quests, slots=2).schedule(0, {})
    assert len(result) == 5
    assert all(x["slot"] in {0, 1} for x in result)


def test_unaffordable_does_not_block_later():
    quests = [
        {"id": "blocked", "duration": 1, "requires": [], "deadline": 10, "cost": {"gold": 99}, "reward": 0},
        {"id": "ok", "duration": 1, "requires": [], "deadline": 10, "cost": {}, "reward": 0},
    ]
    assert [x["id"] for x in scheduler(quests).schedule(0, {})] == ["ok"]
