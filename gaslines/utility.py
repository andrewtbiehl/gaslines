"""
Module that holds miscellaneous, general-purpose utilities used throughout the
gaslines package.
"""


from enum import Enum


class Direction(Enum):
    """
    Two-dimensional vectors representing the four cardinal directions

    It is expected that the order listed here is preserved
    """

    NORTH = (-1, 0)
    EAST = (0, 1)
    SOUTH = (1, 0)
    WEST = (0, -1)


def get_number_of_rows(string):
    """
    Determines the number of rows (a.k.a. lines) contained in the given string. This
    is equivalent to counting one more than the number of newline characters in the
    string.

    Args:
        string (str): The string whose rows are to be counted.
    """
    return len(string.split("\n"))
