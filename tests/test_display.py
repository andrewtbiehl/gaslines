import pytest

from gaslines.display import Cursor, reveal
from gaslines.grid import Grid

# Note: these automated tests merely verify that the functions under test behave
# consistently. Given the functions' visual nature, verification of correct behavior
# initially required manual testing.


UNSOLVED_GRID_STRING = """\
3   ·   ·
         
·   2   ·
         
*   ·   ·\
"""  # noqa: W293


SOLVED_GRID_STRING = """\
3---·---·
        |
·---2   ·
|       |
*---·---·\
"""


@pytest.mark.parametrize("number_of_rows", (1, 2, 11, 101))
def test_move_up_with_positive_number_prints_correct_code(capsys, number_of_rows):
    Cursor.move_up(number_of_rows)
    assert capsys.readouterr().out == f"\x1b[{number_of_rows}A"


@pytest.mark.parametrize("number_of_rows", (0, -1, -2, -11, -101))
def test_move_up_with_non_positive_number_does_nothing(capsys, number_of_rows):
    Cursor.move_up(number_of_rows)
    assert capsys.readouterr().out == ""


def test_clear_below_prints_correct_code(capsys):
    Cursor.clear_below()
    assert capsys.readouterr().out == "\x1b[J"


def test_reveal_with_incomplete_puzzle_prints_and_backtracks(capsys):
    grid = Grid(((3, -1, -1), (-1, 2, -1), (0, -1, -1)))
    # Test reveal with mocked out strategy function and no delay
    reveal(strategy=lambda grid: None, delay=0)(grid)
    assert capsys.readouterr().out == f"\x1b[J{UNSOLVED_GRID_STRING}\n\x1b[5A"


def test_reveal_with_complete_puzzle_prints_but_does_not_backtrack(capsys):
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
    # Test reveal with mocked out strategy function and no delay
    reveal(strategy=lambda grid: None, delay=0)(grid)
    assert capsys.readouterr().out == f"\x1b[J{SOLVED_GRID_STRING}\n"
