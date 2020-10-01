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
