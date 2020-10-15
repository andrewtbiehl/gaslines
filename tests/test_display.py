from gaslines.display import Cursor, print_and_backtrack
import pytest


UNSOLVED_GRID_STRING = """\
3   ·   ·
         
·   2   ·
         
*   ·   ·\
"""


SOLVED_GRID_STRING = """\
3---·---·
        |
·---2   ·
|       |
*---·---·\
"""


# Note: these automated tests merely verify that the functions under test behave
# consistently. Given the functions' visual nature, verification of correct behavior
# initially required manual testing.


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


@pytest.mark.parametrize(
    "input_", ("", "test", UNSOLVED_GRID_STRING, SOLVED_GRID_STRING)
)
def test_print_and_backtrack_with_various_inputs_prints_correctly(capsys, input_):
    lines = len(input_.split("\n"))
    print_and_backtrack(input_)
    assert capsys.readouterr().out == f"\x1b[J{input_}\n\x1b[{lines}A"
