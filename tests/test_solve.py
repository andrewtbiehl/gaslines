"""All unit tests for the gaslines solve module."""


import pytest

from gaslines.grid import Grid
from gaslines.logic import Strategy
from gaslines.solve import solve


REVEAL_SEARCH_STRING = """\
\x1b[J\
2   ·
     
*   *
\x1b[3A\
\x1b[J\
2---·
     
*   *
\x1b[3A\
\x1b[J\
2---·
    |
*   *
"""  # noqa: W293


@pytest.mark.parametrize(
    "strategy", (Strategy.full_recursive, Strategy.partial_recursive)
)
def test_solve_with_trivial_example_solves_grid(strategy):
    """Verifies that `solve` is able to solve a trivial Gas Lines puzzle."""
    grid = Grid(((1, 0),))
    assert solve(grid, strategy)
    assert grid[0][0].child.location == (0, 1)


@pytest.mark.parametrize(
    "strategy", (Strategy.full_recursive, Strategy.partial_recursive)
)
def test_solve_with_simple_example_solves_grid(strategy):
    """Verifies that `solve` is able to solve a simple Gas Lines puzzle."""
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
    """Verifies that `solve` returns false for an unsolvable puzzle."""
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
    """Verifies that `solve` is able to solve the July 12 Gas Lines puzzle."""
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
    """Verifies that `solve` is able to solve the August 9 Gas Lines puzzle."""
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


@pytest.mark.parametrize(
    "strategy", (Strategy.full_recursive, Strategy.partial_recursive)
)
def test_solve_with_reveal_delay_activated_prints_accordingly(strategy, capsys):
    """Verifies that `solve` using the reveal_delay option prints accordingly."""
    grid = Grid(((2, -1), (0, 0)))
    assert solve(grid, strategy, reveal_delay=0)
    assert capsys.readouterr().out == REVEAL_SEARCH_STRING
