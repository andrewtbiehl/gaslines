import pytest

from gaslines.utility import Direction, get_number_of_rows

UNSOLVED_GRID_STRING = """\
3   ·   ·
         
·   2   ·
         
*   ·   ·\
"""  # noqa: W293


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


@pytest.mark.parametrize(
    "input_string,expected_number",
    (("", 1), ("a", 1), ("\n", 2), ("a\nb\nc", 3), (UNSOLVED_GRID_STRING, 5)),
)
def test_get_number_of_rows_with_input_string_returns_expected_number(
    input_string, expected_number
):
    assert get_number_of_rows(input_string) == expected_number
