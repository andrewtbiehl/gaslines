from gaslines.grid import Grid
from gaslines.solve import get_head, has_head


def test_get_head_with_new_puzzle_returns_head():
    grid = Grid(((3, -1, -1), (-1, 2, -1), (0, -1, -1)))
    assert has_head(grid)
    assert get_head(grid).location == (0, 0)


def test_get_head_with_incomplete_puzzle_returns_head():
    grid = Grid(((3, -1, -1), (-1, 2, -1), (0, -1, -1)))
    # Set partial path from "3"
    grid[0][0].child = grid[0][1]
    grid[0][1].child = grid[0][2]
    # Test get_head returns head on path from "3"
    assert has_head(grid)
    assert get_head(grid).location == (0, 2)
    grid[0][2].child = grid[1][2]
    # Test get_head returns head on path from "2"
    assert has_head(grid)
    assert get_head(grid).location == (1, 1)


def test_get_head_with_complete_puzzle_returns_none():
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
    assert not has_head(grid)
    assert get_head(grid) is None
