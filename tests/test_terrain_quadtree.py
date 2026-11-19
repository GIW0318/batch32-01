import pytest

import terrain_quadtree as tq


def tree(budget=8):
    game = tq.TerrainQuadtree(3, budget)
    game.add_patch("near", 0, 0, 10)
    game.add_patch("mid", 30, 0, 10)
    game.add_patch("far", 80, 0, 10)
    return game


def test_near_patch_is_lod0():
    assert tree().select((0, 0)) == [{"id": "near", "lod": 0}]


def test_mid_patch_is_lod1():
    assert tree().select((0, 0)) == [{"id": "mid", "lod": 1}]


def test_far_patch_is_lod2():
    assert tree().select((0, 0)) == [{"id": "far", "lod": 2}]


def test_max_lod_is_capped():
    game = tq.TerrainQuadtree(1, 8)
    game.add_patch("far", 100, 0, 10)
    assert game.select((0, 0))[0]["lod"] == 1


def test_budget_keeps_nearest():
    game = tree(budget=1)
    assert game.select((0, 0)) == [{"id": "near", "lod": 0}]


def test_neighbor_lod_gap_is_clamped():
    game = tq.TerrainQuadtree(3, 8)
    game.add_patch("a", 0, 0, 10, neighbors=["b"])
    game.add_patch("b", 80, 0, 10, neighbors=["a"])
    result = {item["id"]: item["lod"] for item in game.select((0, 0))}
    assert abs(result["a"] - result["b"]) <= 1


def test_neighbor_constraint_propagates():
    game = tq.TerrainQuadtree(3, 8)
    game.add_patch("a", 0, 0, 10, neighbors=["b"])
    game.add_patch("b", 30, 0, 10, neighbors=["a", "c"])
    game.add_patch("c", 80, 0, 10, neighbors=["b"])
    result = {item["id"]: item["lod"] for item in game.select((0, 0))}
    assert result["a"] == 0
    assert result["c"] - result["a"] <= 2


def test_previous_lod_has_hysteresis():
    game = tree()
    previous = {"near": 1, "mid": 1, "far": 2}
    result = {item["id"]: item["lod"] for item in game.select((0, 0), previous)}
    assert result["near"] == 1


def test_duplicate_patch_raises():
    game = tree()
    with pytest.raises(ValueError):
        game.add_patch("near", 1, 1, 10)


def test_invalid_camera_raises():
    with pytest.raises(ValueError):
        tree().select((float("nan"), 0))


def test_invalid_max_lod_raises():
    with pytest.raises(ValueError):
        tq.TerrainQuadtree(-1, 8)


def test_invalid_budget_raises():
    with pytest.raises(ValueError):
        tq.TerrainQuadtree(3, 0)


def test_unknown_neighbor_raises():
    game = tq.TerrainQuadtree(3, 8)
    with pytest.raises(ValueError):
        game.add_patch("a", 0, 0, 10, neighbors=["ghost"])


def test_invalid_patch_size_raises():
    game = tq.TerrainQuadtree(3, 8)
    with pytest.raises(ValueError):
        game.add_patch("a", 0, 0, 0)


def test_output_is_sorted_by_id():
    game = tree()
    ids = [item["id"] for item in game.select((0, 0))]
    assert len(ids) == 3
    assert ids == sorted(ids)
