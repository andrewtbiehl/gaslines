"""All unit tests for the gaslines logic module."""

import itertools

import pytest

from gaslines.grid import Grid
from gaslines.logic import (
    full_recursive,
    get_head,
    get_next,
    has_head,
    is_option,
    partial_recursive,
)


def small_solvable_grid():
    """Test fixture that creates a small and simple solvable Gas Lines puzzle."""
    return Grid(((3, -1, -1), (-1, 2, -1), (0, -1, -1)))


def small_solvable_grid_solution_child_locations():
    """
    Test fixture that returns the solution to the `small_solvable_grid` in the form
    of a matrix of locations of children.
    """
    return (
        ((0, 1), (0, 2), (1, 2)),
        ((2, 0), (1, 0), (2, 2)),
        (None, (2, 0), (2, 1)),
    )


def july_12_grid():
    """Test fixture that creates the July 12 Gas Lines puzzle."""
    # Real NYT Magazine Gas Lines puzzle from the July 12, 2020 issue
    return Grid(
        (
            (3, 3, -1, 6, -1, -1, 2),
            (-1, -1, -1, -1, -1, -1, -1),
            (-1, 0, -1, 2, 0, -1, -1),
            (3, -1, 2, -1, -1, 3, -1),
            (-1, -1, -1, -1, -1, 0, -1),
            (-1, -1, 0, -1, -1, -1, -1),
            (5, -1, -1, 2, -1, -1, -1),
        )
    )


def july_12_grid_solution_child_locations():
    """
    Test fixture that returns the solution to the `july_12_grid` in the form of a
    matrix of locations of children.
    """
    return (
        ((1, 0), (0, 2), (1, 2), (1, 3), (0, 5), (1, 5), (1, 6)),
        ((1, 1), (2, 1), (2, 2), (1, 4), (0, 4), (2, 5), (2, 6)),
        (None, None, (2, 1), (3, 3), None, (2, 4), (3, 6)),
        ((4, 0), (2, 1), (3, 1), (4, 3), (4, 4), (3, 4), (4, 6)),
        ((4, 1), (4, 2), (5, 2), (5, 3), (4, 5), None, (4, 5)),
        ((5, 1), (6, 1), None, (5, 2), None, (4, 5), None),
        ((5, 0), (6, 2), (5, 2), (6, 4), (6, 5), (5, 5), None),
    )


def august_9_grid():
    """Test fixture that creates the August 9 Gas Lines puzzle."""
    # Real NYT Magazine Gas Lines puzzle from the August 9, 2020 issue
    return Grid(
        (
            (2, -1, 0, -1, 2, -1, -1),
            (-1, 4, -1, -1, -1, -1, 4),
            (-1, -1, -1, -1, 2, -1, -1),
            (-1, 0, 1, -1, -1, 0, -1),
            (-1, -1, -1, -1, -1, -1, -1),
            (-1, 3, 0, -1, -1, 4, -1),
            (4, -1, -1, -1, -1, -1, -1),
        )
    )


def august_9_grid_solution_child_locations():
    """
    Test fixture that returns the solution to the `august_9_grid` in the form of a
    matrix of locations of children.
    """
    return (
        ((1, 0), None, None, (0, 2), (0, 5), (1, 5), None),
        ((2, 0), (1, 2), (2, 2), (0, 3), None, (2, 5), (2, 6)),
        ((3, 0), (3, 1), (2, 1), (1, 3), (3, 4), (3, 5), (3, 6)),
        ((3, 1), None, (3, 1), (2, 3), (3, 5), None, (4, 6)),
        ((4, 1), (4, 2), (4, 3), (3, 3), (4, 5), (3, 5), (5, 6)),
        ((4, 0), (6, 1), None, (5, 2), (4, 4), (5, 4), (6, 6)),
        ((5, 0), (6, 2), (5, 2), (5, 3), (6, 3), (6, 4), (6, 5)),
    )


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


@pytest.mark.parametrize("strategy", (full_recursive, partial_recursive))
def test_algorithm_with_trivial_example_solves_grid(strategy):
    """Verifies that each algorithm is able to solve a trivial Gas Lines puzzle."""
    grid = Grid(((1, 0),))
    assert strategy(grid)
    assert grid[0][0].child.location == (0, 1)


@pytest.mark.parametrize("strategy", (full_recursive, partial_recursive))
def test_algorithm_with_unsolvable_example_returns_false(strategy):
    """Verifies that each algorithm returns false for an unsolvable puzzle."""
    grid = Grid(((2, -1, -1), (-1, -1, -1), (-1, -1, -1)))
    assert not strategy(grid)
    # Test that grid is clear
    for row in grid:
        for point in row:
            assert point.is_source() or point.is_open()


@pytest.mark.parametrize("strategy", (full_recursive, partial_recursive))
@pytest.mark.parametrize(
    "grid,expected_child_locations",
    (
        (small_solvable_grid, small_solvable_grid_solution_child_locations),
        (july_12_grid, july_12_grid_solution_child_locations),
        (august_9_grid, august_9_grid_solution_child_locations),
    ),
)
def test_algorithm_with_solvable_example_solves_grid(
    strategy, grid, expected_child_locations
):
    """Verifies that each algorithm is able to solve each provided puzzle."""
    # Call the `grid` and `expected_child_locations` creators during each test
    # Do this to avoid any chance of accidentally reusing a mutable object
    grid = grid()
    expected_child_locations = expected_child_locations()
    assert strategy(grid)
    # Verify the expected child locations one by one
    for i, j in itertools.product(range(grid.height), range(grid.length)):
        point = grid[i][j]
        expected_child_location = expected_child_locations[i][j]
        if expected_child_location is None:
            assert point.is_open()
        else:
            assert point.child.location == expected_child_location
