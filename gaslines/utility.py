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


def index(list_, value):
    """
    Returns the first index of the value if it is present and -1 otherwise.

    This is a simple wrapper function for the list.index() method that, instead of
    raising a ValueError if the value is absent, simply returns -1.
    """
    try:
        return list_.index(value)
    except ValueError:
        return -1
