from gaslines.grid import Grid
from gaslines.solve import get_head, has_head, is_option


def test_get_head_with_new_puzzle_returns_head():
    grid = Grid(((3, -1, -1), (-1, 2, -1), (0, -1, -1)))
    assert has_head(grid)
    assert get_head(grid).location == (0, 0)


def test_get_head_with_incomplete_puzzle_returns_head():
    grid = Grid(((3, -1, -1), (-1, 2, -1), (0, -1, -1)))
    # Set partial path from "3"
    grid[0][0].child = grid[0][1]
    grid[0][1].child = grid[0][2]
    # Test get_head returns head on path from "3"
    assert has_head(grid)
    assert get_head(grid).location == (0, 2)
    grid[0][2].child = grid[1][2]
    # Test get_head returns head on path from "2"
    assert has_head(grid)
    assert get_head(grid).location == (1, 1)


def test_get_head_with_complete_puzzle_returns_none():
    grid = Grid(((3, -1, -1), (-1, 2, -1), (0, -1, -1)))
    # Set path from "3"
    grid[0][0].child = grid[0][1]
    grid[0][1].child = grid[0][2]
    grid[0][2].child = grid[1][2]
    grid[1][2].child = grid[2][2]
    grid[2][2].child = grid[2][1]
    grid[2][1].child = grid[2][0]
    # Set path from "2"
    grid[1][1].child = grid[1][0]
    grid[1][0].child = grid[2][0]
    assert not has_head(grid)
    assert get_head(grid) is None


def test_is_option_with_open_neighbor_returns_true():
    grid = Grid(((3, -1, -1), (-1, 2, -1), (0, -1, -1)))
    current = grid[1][1]
    assert is_option(current, grid[0][1])
    assert is_option(current, grid[1][2])
    assert is_option(current, grid[2][1])
    assert is_option(current, grid[1][0])


def test_is_option_with_unavailable_neighbor_returns_false():
    grid = Grid(((3, -1, -1), (-1, 2, -1), (0, -1, -1)))
    # Set partial path from "3"
    grid[0][0].child = grid[0][1]
    grid[0][1].child = grid[0][2]
    grid[0][2].child = grid[1][2]
    # Test neighbors on partial path from "3"
    current = grid[1][1]
    assert not is_option(current, grid[0][1])
    assert not is_option(current, grid[1][2])


def test_is_option_with_same_segment_and_one_remaining_segment_returns_true():
    grid = Grid(((1, -1, -1, 0), (-1, -1, -1, -1)))
    current = grid[0][1]
    # Set partial path to current
    grid[0][0].child = current
    assert is_option(current, grid[0][2])


def test_is_option_with_new_segment_and_one_remaining_segment_returns_false():
    grid = Grid(((1, -1, -1, 0), (-1, -1, -1, -1)))
    current = grid[0][1]
    # Set partial path to current
    grid[0][0].child = current
    assert not is_option(current, grid[1][1])


def test_is_option_with_same_segment_sink_and_one_remaining_segment_returns_true():
    grid = Grid(((1, -1, 0), (-1, 0, -1)))
    current = grid[0][1]
    # Set partial path to current
    grid[0][0].child = current
    assert is_option(current, grid[0][2])


def test_is_option_with_new_segment_sink_and_one_remaining_segment_returns_false():
    grid = Grid(((1, -1, 0), (-1, 0, -1)))
    current = grid[0][1]
    # Set partial path to current
    grid[0][0].child = current
    assert not is_option(current, grid[1][1])


def test_is_option_with_same_segment_sink_and_two_remaining_segments_returns_false():
    grid = Grid(((2, -1, 0), (-1, 0, -1)))
    current = grid[0][1]
    # Set partial path to current
    grid[0][0].child = current
    assert not is_option(current, grid[0][2])


def test_is_option_with_new_segment_sink_and_two_remaining_segments_returns_true():
    grid = Grid(((2, -1, 0), (-1, 0, -1)))
    current = grid[0][1]
    # Set partial path to current
    grid[0][0].child = current
    assert is_option(current, grid[1][1])


def test_is_option_with_sink_and_greater_than_two_remaining_segments_returns_false():
    grid = Grid(((-1, 0, -1), (3, -1, 0), (-1, -1, 0)))
    current = grid[1][1]
    # Set partial path to current
    grid[1][0].child = current
    # Test sink on same segment
    assert not is_option(current, grid[0][1])
    # Test sink on new segment
    assert not is_option(current, grid[1][2])
