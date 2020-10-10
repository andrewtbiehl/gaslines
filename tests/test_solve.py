from gaslines.grid import Grid
from gaslines.solve import get_head, has_head, is_option, get_next, Strategy, solve
import pytest


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


def test_get_next_with_no_child_and_all_open_neighbors_returns_first_available():
    grid = Grid(((3, -1, -1), (-1, 2, -1), (0, -1, -1)))
    assert get_next(grid[0][0]).location == (0, 1)
    assert get_next(grid[1][1]).location == (0, 1)


def test_get_next_with_no_child_and_some_open_neighbors_returns_first_available():
    grid = Grid(((3, -1, -1), (-1, 2, -1), (0, -1, -1)))
    # Set partial path from "3"
    grid[0][0].child = grid[0][1]
    grid[0][1].child = grid[0][2]
    grid[0][2].child = grid[1][2]
    assert get_next(grid[1][1]).location == (2, 1)


def test_get_next_with_no_child_and_no_open_neighbors_returns_none():
    grid = Grid(((4, -1, 1), (0, -1, -1), (-1, -1, 0)))
    # Set (incorrect) path from "4"
    grid[0][0].child = grid[0][1]
    grid[0][1].child = grid[1][1]
    grid[1][1].child = grid[1][2]
    grid[1][2].child = grid[2][2]
    assert get_next(grid[1][2]) is None


def test_get_next_with_one_remaining_segment_skips_point_on_new_segment():
    grid = Grid(((-1, -1, -1, -1), (1, -1, -1, 0)))
    grid[1][0].child = grid[1][1]
    assert get_next(grid[1][1]).location == (1, 2)


def test_get_next_with_two_remaining_segments_skips_sink_on_same_segment():
    grid = Grid(((2, -1, 0), (-1, 0, -1)))
    current = grid[0][1]
    # Set partial path to current
    grid[0][0].child = current
    assert get_next(current).location == (1, 1)


def test_get_next_with_greater_than_two_remaining_segments_skips_sinks():
    grid = Grid(((-1, 0, -1), (4, -1, 0), (-1, -1, -1)))
    current = grid[1][1]
    # Set partial path to current
    grid[1][0].child = current
    assert get_next(current).location == (2, 1)


def test_get_next_with_first_of_multiple_children_returns_next_child():
    grid = Grid(((3, -1, -1), (-1, 2, -1), (0, -1, -1)))
    grid[1][1].child = grid[0][1]
    assert get_next(grid[1][1]).location == (1, 2)


def test_get_next_with_last_child_returns_none():
    grid = Grid(((3, -1, -1), (-1, 2, -1), (0, -1, -1)))
    grid[1][1].child = grid[1][0]
    assert get_next(grid[1][1]) is None


@pytest.mark.parametrize(
    "strategy", (Strategy.full_recursive, Strategy.partial_recursive)
)
def test_solve_with_trivial_example_solves_grid(strategy):
    grid = Grid(((1, 0),))
    assert solve(grid, strategy)
    assert grid[0][0].child.location == (0, 1)


@pytest.mark.parametrize(
    "strategy", (Strategy.full_recursive, Strategy.partial_recursive)
)
def test_solve_with_simple_example_solves_grid(strategy):
    grid = Grid(((3, -1, -1), (-1, 2, -1), (0, -1, -1)))
    assert solve(grid, strategy)
    # Test all points in component-wise order
    assert grid[0][0].child.location == (0, 1)
    assert grid[0][1].child.location == (0, 2)
    assert grid[0][2].child.location == (1, 2)
    assert grid[1][0].child.location == (2, 0)
    assert grid[1][1].child.location == (1, 0)
    assert grid[1][2].child.location == (2, 2)
    assert grid[2][0].is_open()
    assert grid[2][1].child.location == (2, 0)
    assert grid[2][2].child.location == (2, 1)


@pytest.mark.parametrize(
    "strategy", (Strategy.full_recursive, Strategy.partial_recursive)
)
def test_solve_with_unsolvable_example_returns_false(strategy):
    grid = Grid(((2, -1, -1), (-1, -1, -1), (-1, -1, -1)))
    assert not solve(grid, strategy)
    # Test that grid is clear
    for row in grid:
        for point in row:
            assert point.is_source() or point.is_open()


@pytest.mark.parametrize(
    "strategy", (Strategy.full_recursive, Strategy.partial_recursive)
)
def test_solve_with_real_july_12_example_solves_grid(strategy):
    # Real NYT Magazine Gas Lines puzzle from the July 12, 2020 issue
    grid = Grid(
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
    assert solve(grid, strategy)
    # Test all points in component-wise order
    assert grid[0][0].child.location == (1, 0)
    assert grid[0][1].child.location == (0, 2)
    assert grid[0][2].child.location == (1, 2)
    assert grid[0][3].child.location == (1, 3)
    assert grid[0][4].child.location == (0, 5)
    assert grid[0][5].child.location == (1, 5)
    assert grid[0][6].child.location == (1, 6)
    assert grid[1][0].child.location == (1, 1)
    assert grid[1][1].child.location == (2, 1)
    assert grid[1][2].child.location == (2, 2)
    assert grid[1][3].child.location == (1, 4)
    assert grid[1][4].child.location == (0, 4)
    assert grid[1][5].child.location == (2, 5)
    assert grid[1][6].child.location == (2, 6)
    assert grid[2][0].is_open()
    assert grid[2][1].is_open()
    assert grid[2][2].child.location == (2, 1)
    assert grid[2][3].child.location == (3, 3)
    assert grid[2][4].is_open()
    assert grid[2][5].child.location == (2, 4)
    assert grid[2][6].child.location == (3, 6)
    assert grid[3][0].child.location == (4, 0)
    assert grid[3][1].child.location == (2, 1)
    assert grid[3][2].child.location == (3, 1)
    assert grid[3][3].child.location == (4, 3)
    assert grid[3][4].child.location == (4, 4)
    assert grid[3][5].child.location == (3, 4)
    assert grid[3][6].child.location == (4, 6)
    assert grid[4][0].child.location == (4, 1)
    assert grid[4][1].child.location == (4, 2)
    assert grid[4][2].child.location == (5, 2)
    assert grid[4][3].child.location == (5, 3)
    assert grid[4][4].child.location == (4, 5)
    assert grid[4][5].is_open()
    assert grid[4][6].child.location == (4, 5)
    assert grid[5][0].child.location == (5, 1)
    assert grid[5][1].child.location == (6, 1)
    assert grid[5][2].is_open()
    assert grid[5][3].child.location == (5, 2)
    assert grid[5][4].is_open()
    assert grid[5][5].child.location == (4, 5)
    assert grid[5][6].is_open()
    assert grid[6][0].child.location == (5, 0)
    assert grid[6][1].child.location == (6, 2)
    assert grid[6][2].child.location == (5, 2)
    assert grid[6][3].child.location == (6, 4)
    assert grid[6][4].child.location == (6, 5)
    assert grid[6][5].child.location == (5, 5)
    assert grid[6][6].is_open()


@pytest.mark.parametrize(
    "strategy", (Strategy.full_recursive, Strategy.partial_recursive)
)
def test_solve_with_real_august_9_example_solves_grid(strategy):
    # Real NYT Magazine Gas Lines puzzle from the August 9, 2020 issue
    grid = Grid(
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
    assert solve(grid, strategy)
    # Test all points in component-wise order
    assert grid[0][0].child.location == (1, 0)
    assert grid[0][1].is_open()
    assert grid[0][2].is_open()
    assert grid[0][3].child.location == (0, 2)
    assert grid[0][4].child.location == (0, 5)
    assert grid[0][5].child.location == (1, 5)
    assert grid[0][6].is_open()
    assert grid[1][0].child.location == (2, 0)
    assert grid[1][1].child.location == (1, 2)
    assert grid[1][2].child.location == (2, 2)
    assert grid[1][3].child.location == (0, 3)
    assert grid[1][4].is_open()
    assert grid[1][5].child.location == (2, 5)
    assert grid[1][6].child.location == (2, 6)
    assert grid[2][0].child.location == (3, 0)
    assert grid[2][1].child.location == (3, 1)
    assert grid[2][2].child.location == (2, 1)
    assert grid[2][3].child.location == (1, 3)
    assert grid[2][4].child.location == (3, 4)
    assert grid[2][5].child.location == (3, 5)
    assert grid[2][6].child.location == (3, 6)
    assert grid[3][0].child.location == (3, 1)
    assert grid[3][1].is_open()
    assert grid[3][2].child.location == (3, 1)
    assert grid[3][3].child.location == (2, 3)
    assert grid[3][4].child.location == (3, 5)
    assert grid[3][5].is_open()
    assert grid[3][6].child.location == (4, 6)
    assert grid[4][0].child.location == (4, 1)
    assert grid[4][1].child.location == (4, 2)
    assert grid[4][2].child.location == (4, 3)
    assert grid[4][3].child.location == (3, 3)
    assert grid[4][4].child.location == (4, 5)
    assert grid[4][5].child.location == (3, 5)
    assert grid[4][6].child.location == (5, 6)
    assert grid[5][0].child.location == (4, 0)
    assert grid[5][1].child.location == (6, 1)
    assert grid[5][2].is_open()
    assert grid[5][3].child.location == (5, 2)
    assert grid[5][4].child.location == (4, 4)
    assert grid[5][5].child.location == (5, 4)
    assert grid[5][6].child.location == (6, 6)
    assert grid[6][0].child.location == (5, 0)
    assert grid[6][1].child.location == (6, 2)
    assert grid[6][2].child.location == (5, 2)
    assert grid[6][3].child.location == (5, 3)
    assert grid[6][4].child.location == (6, 3)
    assert grid[6][5].child.location == (6, 4)
    assert grid[6][6].child.location == (6, 5)
