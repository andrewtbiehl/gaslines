"""
Module that holds the `solve` function, whose purpose is to pull together the various
features of this project into a single interface to interact with when solving a Gas
Lines puzzle.
"""


import functools

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
    # Optionally reveal the grid while it is being solved
    if reveal_delay is not None:
        # Reveal the grid once after each mutation
        reveal = functools.partial(display.reveal, grid, reveal_delay)
        grid.register(reveal)
        # Also reveal the grid in its initial state, prior to solving it
        reveal()
    return strategy(grid)
