"""
Module that holds utilities specifically used to visualize Gas Lines puzzles and
solutions in a standard terminal.
"""


import time

from gaslines.logic import has_head
from gaslines.utility import get_number_of_rows


def reveal(grid, delay):
    """
    In a standard terminal, briefly displays a given Gas Lines grid in its current
    state while also preparing for future invocation once the grid has been updated.

    In practice, this function is used to display intermediate search results in real
    time while solving a given Gas Lines grid.

    Args:
        grid (Grid): The Gas Lines grid to reveal.
        delay (float): Amount of time (in seconds) to artificially delay after
            revealing the grid.
    """
    grid_image = str(grid)
    # Clear all rows below the cursor, print the grid, pause, and then backtrack
    Cursor.clear_below()
    print(grid_image)
    time.sleep(delay)
    if has_head(grid):
        Cursor.move_up(get_number_of_rows(grid_image))


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
