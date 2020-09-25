import pytest
from gaslines.utility import Direction


def test_direction_returns_valid_direction():
    assert Direction.NORTH.value == (-1, 0)
    assert Direction.EAST.value == (0, 1)
    assert Direction.SOUTH.value == (1, 0)
    assert Direction.WEST.value == (0, -1)


def test_list_returns_expected_direction_order():
    assert list(Direction) == [
        Direction.NORTH,
        Direction.EAST,
        Direction.SOUTH,
        Direction.WEST,
    ]
