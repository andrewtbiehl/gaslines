"""
Module that holds utilities specifically used to visualize Gas Lines puzzles and
solutions in a standard terminal.
"""


import time

from gaslines.logic import has_head
from gaslines.utility import get_number_of_rows


def reveal(strategy, delay):
    """
    Wraps the given strategy function with the additional functionality of displaying
    intermediate search results in real time while solving a given Gas Lines grid.

    Args:
        strategy (Strategy class method): An algorithm for solving a Gas Lines grid.
        delay (float): Amount of time (in seconds) to artificially delay between each
            intermediate stage of the search.
    """

    def wrapper(grid, *args, **kwargs):
        grid_image = str(grid)
        # Clear all rows below the cursor, print the grid, pause, and then backtrack
        Cursor.clear_below()
        print(grid_image)
        time.sleep(delay)
        if has_head(grid):
            Cursor.move_up(get_number_of_rows(grid_image))
        return strategy(grid, *args, **kwargs)

    return wrapper


class Cursor:
    """
    Static class that holds functions that wrap more complex interactions with a
    standard terminal.
    """

    # Credit to the blessings terminal library, the inspection of which helped with
    # the implementation of these methods

    @staticmethod
    def move_up(number_of_rows):
        """
        Moves the terminal cursor up from its current location the number of rows
        specified.

        Args:
            number_of_rows (int): The number of rows to move up. Negative values are
                ignored.
        """
        if number_of_rows > 0:
            # Prints a particular ANSI escape code for the desired outcome
            print(f"\x1b[{number_of_rows}A", end="")

    @staticmethod
    def clear_below():
        """
        Clears all rows below the cursor's current location (inclusive).
        """
        # Prints a particular ANSI escape code for the desired outcome
        print("\x1b[J", end="")
