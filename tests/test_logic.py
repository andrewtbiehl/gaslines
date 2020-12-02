"""All unit tests for the gaslines logic module."""


from gaslines.grid import Grid
from gaslines.logic import get_head, get_next, has_head, is_option


def test_get_head_with_new_puzzle_returns_head():
    """Verifies that `get_head` on a completely unsolved puzzle returns a head."""
    grid = Grid(((3, -1, -1), (-1, 2, -1), (0, -1, -1)))
    assert has_head(grid)
    assert get_head(grid).location == (0, 0)


def test_get_head_with_incomplete_puzzle_returns_head():
    """Verifies that `get_head` on a partially solved puzzle returns a head."""
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
    """Verifies that a completely solved puzzle reports having no heads."""
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
    """Verifies that `is_option` correctly identifies when a point is an option."""
    grid = Grid(((3, -1, -1), (-1, 2, -1), (0, -1, -1)))
    current = grid[1][1]
    assert is_option(current, grid[0][1])
    assert is_option(current, grid[1][2])
    assert is_option(current, grid[2][1])
    assert is_option(current, grid[1][0])


def test_is_option_with_unavailable_neighbor_returns_false():
    """
    Verifies that `is_option` correctly identifies when a point is not an option.
    """
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
    """Verifies that a point on the last allowed segment is an option."""
    grid = Grid(((1, -1, -1, 0), (-1, -1, -1, -1)))
    current = grid[0][1]
    # Set partial path to current
    grid[0][0].child = current
    assert is_option(current, grid[0][2])


def test_is_option_with_new_segment_and_one_remaining_segment_returns_false():
    """Verifies that a point not on the last allowed segment is not an option."""
    grid = Grid(((1, -1, -1, 0), (-1, -1, -1, -1)))
    current = grid[0][1]
    # Set partial path to current
    grid[0][0].child = current
    assert not is_option(current, grid[1][1])


def test_is_option_with_same_segment_sink_and_one_remaining_segment_returns_true():
    """Verifies that a sink on the last allowed segment is an option."""
    grid = Grid(((1, -1, 0), (-1, 0, -1)))
    current = grid[0][1]
    # Set partial path to current
    grid[0][0].child = current
    assert is_option(current, grid[0][2])


def test_is_option_with_new_segment_sink_and_one_remaining_segment_returns_false():
    """Verifies that a sink not on the last allowed segment is not an option."""
    grid = Grid(((1, -1, 0), (-1, 0, -1)))
    current = grid[0][1]
    # Set partial path to current
    grid[0][0].child = current
    assert not is_option(current, grid[1][1])


def test_is_option_with_same_segment_sink_and_two_remaining_segments_returns_false():
    """Verifies that a sink on the second to last allowed segment is not an option."""
    grid = Grid(((2, -1, 0), (-1, 0, -1)))
    current = grid[0][1]
    # Set partial path to current
    grid[0][0].child = current
    assert not is_option(current, grid[0][2])


def test_is_option_with_new_segment_sink_and_two_remaining_segments_returns_true():
    """Verifies that a sink not on the second to last allowed segment is an option."""
    grid = Grid(((2, -1, 0), (-1, 0, -1)))
    current = grid[0][1]
    # Set partial path to current
    grid[0][0].child = current
    assert is_option(current, grid[1][1])


def test_is_option_with_sink_and_greater_than_two_remaining_segments_returns_false():
    """
    Verifies that, with more than two remaining segments, a sink is not an option.
    """
    grid = Grid(((-1, 0, -1), (3, -1, 0), (-1, -1, 0)))
    current = grid[1][1]
    # Set partial path to current
    grid[1][0].child = current
    # Test sink on same segment
    assert not is_option(current, grid[0][1])
    # Test sink on new segment
    assert not is_option(current, grid[1][2])


def test_get_next_with_no_child_and_all_open_neighbors_returns_first_available():
    """
    Verifies that `get_next` returns the first available neighbor if all are open.
    """
    grid = Grid(((3, -1, -1), (-1, 2, -1), (0, -1, -1)))
    assert get_next(grid[0][0]).location == (0, 1)
    assert get_next(grid[1][1]).location == (0, 1)


def test_get_next_with_no_child_and_some_open_neighbors_returns_first_available():
    """
    Verifies that `get_next` returns the first available neighbor if some are open.
    """
    grid = Grid(((3, -1, -1), (-1, 2, -1), (0, -1, -1)))
    # Set partial path from "3"
    grid[0][0].child = grid[0][1]
    grid[0][1].child = grid[0][2]
    grid[0][2].child = grid[1][2]
    assert get_next(grid[1][1]).location == (2, 1)


def test_get_next_with_no_child_and_no_open_neighbors_returns_none():
    """Verifies that `get_next` returns None if no neighbors are open."""
    grid = Grid(((4, -1, 1), (0, -1, -1), (-1, -1, 0)))
    # Set (incorrect) path from "4"
    grid[0][0].child = grid[0][1]
    grid[0][1].child = grid[1][1]
    grid[1][1].child = grid[1][2]
    grid[1][2].child = grid[2][2]
    assert get_next(grid[1][2]) is None


def test_get_next_with_one_remaining_segment_skips_point_on_new_segment():
    """
    Verifies that `get_next`, on last allowed segment, skips points on new segments.
    """
    grid = Grid(((-1, -1, -1, -1), (1, -1, -1, 0)))
    grid[1][0].child = grid[1][1]
    assert get_next(grid[1][1]).location == (1, 2)


def test_get_next_with_two_remaining_segments_skips_sink_on_same_segment():
    """
    Verifies that `get_next` skips a sink not on the last allowed segment.
    """
    grid = Grid(((2, -1, 0), (-1, 0, -1)))
    current = grid[0][1]
    # Set partial path to current
    grid[0][0].child = current
    assert get_next(current).location == (1, 1)


def test_get_next_with_greater_than_two_remaining_segments_skips_sinks():
    """
    Verifies that `get_next` skips a sink not on the last allowed segment.
    """
    grid = Grid(((-1, 0, -1), (4, -1, 0), (-1, -1, -1)))
    current = grid[1][1]
    # Set partial path to current
    grid[1][0].child = current
    assert get_next(current).location == (2, 1)


def test_get_next_with_first_of_multiple_children_returns_next_child():
    """
    Verifies that `get_next` on a point with a child returns the correct next point.
    """
    grid = Grid(((3, -1, -1), (-1, 2, -1), (0, -1, -1)))
    grid[1][1].child = grid[0][1]
    assert get_next(grid[1][1]).location == (1, 2)


def test_get_next_with_last_child_returns_none():
    """
    Verifies that `get_next` on a point with its last possible child returns None.
    """
    grid = Grid(((3, -1, -1), (-1, 2, -1), (0, -1, -1)))
    grid[1][1].child = grid[1][0]
    assert get_next(grid[1][1]) is None
