"""All unit tests for the gaslines grid module."""


import pytest

from gaslines.grid import Grid


GRID_STRING_1 = """\
3   ·   ·
         
·   2   ·
         
*   ·   ·\
"""  # noqa: W293

GRID_STRING_2 = """\
3---·---·
        |
·---2   ·
|       |
*---·---·\
"""


class Incrementor:
    """
    A simple class that initializes an integer value at zero and then, whenever
    directed, increments that value by one.
    """

    def __init__(self):
        self._count = 0

    def increment(self):
        """Increments the count."""
        self._count += 1

    @property
    def count(self):
        """Returns the current count."""
        return self._count


@pytest.mark.parametrize(
    "input_grid", (((-1,), (-1,)), ((1, 0), (-1, -1)), ((-1,), (-1,), (-1,)))
)
def test_dimensions_return_dimensions_when_asked(input_grid):
    """Verifies that the height and length properties return the correct values."""
    output_grid = Grid(input_grid)
    assert output_grid.height == len(input_grid)
    assert output_grid.length == len(input_grid[0])


def test_subscripting_returns_correct_points():
    """Verifies that the subscript operator works as expected."""
    grid = Grid(
        (
            (-1, -1, -1),
            (0, 0, 0),
            (1, 2, 3),
        )
    )
    # Test that each row contains three points
    for i in range(3):
        assert len(grid[i]) == 3
    # Test that we cannot access nonexistent rows
    with pytest.raises(IndexError):
        grid[3]
    # Test that the first row only has pipes
    for point in grid[0]:
        assert not point.is_source() and not point.is_sink()
    # Test that the second row only has sinks
    for point in grid[1]:
        assert point.is_sink()
    # Test that the third row only has sources
    for point in grid[2]:
        assert point.is_source()


def test_str_with_empty_board_returns_correct_string():
    """Verifies that the string representation of an unsolved grid is correct."""
    grid = Grid(((3, -1, -1), (-1, 2, -1), (0, -1, -1)))
    assert str(grid) == GRID_STRING_1


def test_str_with_complete_board_returns_correct_string():
    """Verifies that the string representation of a solved grid is correct."""
    grid = Grid(((3, -1, -1), (-1, 2, -1), (0, -1, -1)))
    # Set path from "3"
    grid[0][0].child = grid[0][1]
    grid[0][1].child = grid[0][2]
    grid[0][2].child = grid[1][2]
    grid[1][2].child = grid[2][2]
    grid[2][2].child = grid[2][1]
    grid[2][1].child = grid[2][0]
    # Set path from "2"
    grid[1][1].child = grid[1][0]
    grid[1][0].child = grid[2][0]
    assert str(grid) == GRID_STRING_2


def test_observability_with_point_mutations_notifies_observers():
    """Verifies that grids forward point mutation notifications to their observers"""
    grid = Grid(((-1, -1), (-1, -1)))
    point = grid[0][0]
    # Instantiate and register an incrementor as an example observer of the grid
    incrementor = Incrementor()
    grid.register(incrementor.increment)
    # Mutate a point on the grid an arbitrary number of times
    # Verify that the incrementor indeed increments in response to each point mutation
    assert incrementor.count == 0
    for i in range(1, 4):
        # Solely accessing the point's child field should not notify observers
        assert point.child is None
        # Mutating the point's child field should indeed notify observers
        point.child = None
        assert incrementor.count == i
