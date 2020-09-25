import pytest
from gaslines.grid import Grid


@pytest.mark.parametrize(
    "input_grid", (((-1,), (-1,)), ((1, 0), (-1, -1)), ((-1,), (-1,), (-1,)))
)
def test_dimensions_return_dimensions_when_asked(input_grid):
    output_grid = Grid(input_grid)
    assert output_grid.height == len(input_grid)
    assert output_grid.length == len(input_grid[0])


def test_subscripting_returns_correct_points():
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
