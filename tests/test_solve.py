"""All unit tests for the gaslines solve module."""


import pytest

from gaslines.grid import Grid
from gaslines.logic import full_recursive, partial_recursive
from gaslines.solve import solve
from tests.utility import draw_path


REVEAL_SEARCH_STRING = """\
\x1b[J\
2   ·
     \n\
*   *
\x1b[3A\
\x1b[J\
2---·
     \n\
*   *
\x1b[3A\
\x1b[J\
2---·
    |
*   *
"""


def mock_strategy(grid):
    """
    Mock algorithm to be applied only to the following grid:

    2   ·

    *   *
    """
    draw_path(grid, ((0, 0), (0, 1), (1, 1)))
    return True


def test_solve_with_reveal_delay_deactivated_is_silent(capsys):
    """Verifies that `solve` prints nothing when reveal_delay is set to None."""
    grid = Grid(((2, -1), (0, 0)))
    assert solve(grid, strategy=mock_strategy, reveal_delay=None)
    assert capsys.readouterr().out == ""


def test_solve_with_reveal_delay_activated_prints_accordingly(capsys):
    """Verifies that `solve` using the reveal_delay option prints accordingly."""
    grid = Grid(((2, -1), (0, 0)))
    assert solve(grid, strategy=mock_strategy, reveal_delay=0)
    assert capsys.readouterr().out == REVEAL_SEARCH_STRING


def test_solve_with_default_arguments_solves_grid_silently(capsys):
    """Verifies that `solve` using default arguments solves a real grid silently."""
    grid = Grid(((2, -1), (0, 0)))
    assert solve(grid)
    # Test all points in component-wise order
    assert grid[0][0].child.location == (0, 1)
    assert grid[0][1].child.location == (1, 1)
    assert grid[1][0].is_open()
    assert grid[1][1].is_open()
    # Verify that nothing was printed to the console
    assert capsys.readouterr().out == ""


@pytest.mark.parametrize("strategy", (full_recursive, partial_recursive))
def test_solve_with_real_strategies_solves_grid(strategy):
    """Verifies that `solve` using real strategies solves a real grid."""
    grid = Grid(((2, -1), (0, 0)))
    assert solve(grid, strategy=strategy)
    # Test all points in component-wise order
    assert grid[0][0].child.location == (0, 1)
    assert grid[0][1].child.location == (1, 1)
    assert grid[1][0].is_open()
    assert grid[1][1].is_open()
