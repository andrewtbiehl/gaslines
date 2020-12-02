"""
Module that holds the `solve` function, whose purpose is to pull together the various
features of this project into a single interface to interact with when solving a Gas
Lines puzzle.
"""


import gaslines.display as display
from gaslines.logic import Strategy


def solve(grid, strategy=Strategy.full_recursive, reveal_delay=None):
    """
    Solves a Gas Lines puzzle (using the strategy provided).

    Mutates the grid object provided to search for a solution and returns True once a
    solution has been found or False if no solution exists.

    Args:
        grid (Grid): A (presumably unsolved) Gas Lines grid.
        strategy (Strategy class method): The choice of algorithm with which to solve
            the grid. Defaults to the "full_recursive" strategy.
        reveal_delay (float, NoneType): If not None, displays intermediate stages of
            the search, pausing between each stage for the given number of seconds.
            Defaults to None.

    Returns:
        bool: Whether the grid has a solution.
    """
    strategy_name = strategy.__name__
    strategy_container = Strategy()
    solve = getattr(strategy_container, strategy_name)
    # Optionally decorate the algorithm with reveal functionality
    if reveal_delay is not None:
        solve = display.reveal(solve, reveal_delay)
        setattr(strategy_container, strategy_name, solve)
    return solve(grid)
