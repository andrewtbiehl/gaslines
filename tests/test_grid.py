import pytest
from gaslines.grid import Grid


@pytest.mark.parametrize(
    "input_grid", (((-1,), (-1,)), ((1, 0), (-1, -1)), ((-1,), (-1,), (-1,)))
)
def test_dimensions_return_dimensions_when_asked(input_grid):
    output_grid = Grid(input_grid)
    assert output_grid.height == len(input_grid)
    assert output_grid.length == len(input_grid[0])
