import pytest
from gaslines.utility import Direction
from gaslines.utility import index


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


def test_index_with_value_present_returns_index():
    list_ = ["a", "b", "c", "d"]
    for i, value in enumerate(list_):
        assert index(list_, value) == list_.index(value) == i


def test_index_with_value_absent_returns_negative_one():
    list_ = ["a", "b", "c", "d"]
    assert index(list_, "e") == -1
