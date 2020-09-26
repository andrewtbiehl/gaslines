import pytest
from gaslines.point import Point
from gaslines.grid import Grid
from gaslines.utility import Direction


@pytest.mark.parametrize("grid", (None, [[0, 1], [None, None]], ((0, 1), (None, None))))
def test_grid_returns_grid_when_asked(grid):
    point = Point(grid, None)
    assert point.grid == grid


@pytest.mark.parametrize("location", (None, [0, 1], (0, 1)))
def test_location_returns_location_when_asked(location):
    point = Point(None, location)
    assert point.location == location


@pytest.mark.parametrize("row_index,column_index", ((0, 0), (0, 1), (1, 2)))
def test_indexes_return_correct_values_when_asked(row_index, column_index):
    point = Point(None, (row_index, column_index))
    assert point.row_index == row_index
    assert point.column_index == column_index


@pytest.mark.parametrize("type_", (1, 2, 3, 9, 45))
def test_is_source_returns_true_when_is_source(type_):
    point = Point(None, None, type_)
    assert point.is_source()


@pytest.mark.parametrize("type_", (-1, 0, Point.PIPE, Point.SINK))
def test_is_source_returns_false_when_is_not_source(type_):
    point = Point(None, None, type_)
    assert not point.is_source()


@pytest.mark.parametrize("type_", (0, Point.SINK))
def test_is_sink_returns_true_when_is_sink(type_):
    point = Point(None, None, type_)
    assert point.is_sink()


@pytest.mark.parametrize("type_", (-1, 1, 2, 3, 9, 45, Point.PIPE))
def test_is_sink_returns_false_when_is_not_sink(type_):
    point = Point(None, None, type_)
    assert not point.is_sink()


def test_init_sets_pipe_when_no_type_provided():
    point = Point(None, None)
    assert not point.is_source()
    assert not point.is_sink()


def test_child_returns_child_when_provided_child():
    point = Point(None, None)
    child = Point(None, None)
    point.child = child
    assert point.has_child()
    assert point.child == child


def test_child_returns_no_child_when_not_provided_child():
    point = Point(None, None)
    assert not point.has_child()
    assert point.child is None


def test_child_returns_no_child_when_child_reset():
    point = Point(None, None)
    child = Point(None, None)
    # Test that child set correctly
    point.child = child
    assert point.has_child()
    assert point.child == child
    # Test that child reset correctly
    point.child = None
    assert not point.has_child()
    assert point.child is None


def test_get_neighbor_with_neighbor_present_returns_correct_point():
    # The types have been carefully assigned for ease of testing
    grid = Grid(((0, 1, 0), (4, 5, 2), (0, 3, 0)))
    point = grid[1][1]
    assert point._type == 5
    # Test that the correct neighbor exists in each direction
    for i, direction in enumerate(Direction):
        assert point.has_neighbor(direction)
        neighbor = point.get_neighbor(direction)
        assert neighbor._type == i + 1


def test_get_neighbor_with_missing_neighbor_returns_none():
    # The types have been carefully assigned for ease of testing
    grid = Grid(((1, 2, 0), (0, 0, 3), (0, 0, 4)))
    # Test the north west point
    point = grid[0][0]
    assert point._type == 1
    assert not (
        point.has_neighbor(Direction.NORTH) or point.has_neighbor(Direction.WEST)
    )
    assert point.get_neighbor(Direction.NORTH) is None
    # Test the north center point
    point = grid[0][1]
    assert point._type == 2
    assert not point.has_neighbor(Direction.NORTH)
    assert point.get_neighbor(Direction.NORTH) is None
    # Test the center east point
    point = grid[1][2]
    assert point._type == 3
    assert not point.has_neighbor(Direction.EAST)
    assert point.get_neighbor(Direction.EAST) is None
    # Test the south east point
    point = grid[2][2]
    assert point._type == 4
    assert not (
        point.has_neighbor(Direction.EAST) or point.has_neighbor(Direction.EAST)
    )
    assert point.get_neighbor(Direction.EAST) is None


def test_get_neighbors_with_some_neighbors_returns_correct_points():
    grid = Grid(((1, 2), (3, 0)))
    point = grid[0][0]
    assert point._type == 1
    neighbors = point.get_neighbors()
    assert len(neighbors) == 2
    assert [point._type for point in neighbors] == [2, 3]


def test_parent_with_parent_returns_correct_point():
    grid = Grid(((2, -1), (1, 0)))
    parent, child = grid[0][0], grid[0][1]
    parent.child = child
    assert child.has_parent()
    assert child.parent is parent


def test_parent_with_no_parent_returns_none():
    grid = Grid(((2, -1), (1, 0)))
    point = grid[0][1]
    assert not point.has_parent()
    assert point.parent is None


def test_parent_with_sink_returns_none():
    grid = Grid(((2, -1), (1, 0)))
    source, pipe, sink = grid[0][0], grid[0][1], grid[1][1]
    source.child = pipe
    pipe.child = sink
    assert not sink.has_parent()
    assert sink.parent is None


def test_is_open_with_source_returns_false():
    grid = Grid(((2, -1), (1, 0)))
    assert not grid[0][0].is_open()


def test_is_open_with_sink_returns_true():
    grid = Grid(((2, -1), (1, 0)))
    sink = grid[1][1]
    # Test sink is open with no "parents"
    assert sink.is_open()
    # Test sink is open with one "parent"
    grid[0][0].child = grid[0][1]
    grid[0][1].child = sink
    assert sink.is_open()
    # Test sink is open with two "parents"
    grid[1][0].child = sink
    assert sink.is_open()


def test_is_open_with_pipe_conditional_on_parent():
    grid = Grid(((2, -1), (1, 0)))
    pipe = grid[0][1]
    # Test pipe without parent is open
    assert pipe.is_open()
    # Test pipe with parent is not open
    grid[0][0].child = pipe
    assert not pipe.is_open()


def test_is_on_new_segment_with_source_returns_false():
    grid = Grid(((2, -1, -1), (-1, -1, -1), (1, -1, 0)))
    assert not grid[0][0].is_on_new_segment()
    assert not grid[2][0].is_on_new_segment()


def test_is_on_new_segment_with_open_point_returns_false():
    grid = Grid(((2, -1, -1), (-1, -1, -1), (1, -1, 0)))
    assert not grid[0][1].is_on_new_segment()
    assert not grid[1][1].is_on_new_segment()
    assert not grid[1][2].is_on_new_segment()


def test_is_on_new_segment_with_sink_returns_false():
    grid = Grid(((2, -1, -1), (-1, -1, -1), (1, -1, 0)))
    sink = grid[2][2]
    # Test sink with no parents
    assert not sink.is_on_new_segment()
    # Test sink with one parent
    grid[0][0].child = grid[0][1]
    grid[0][1].child = grid[0][2]
    grid[0][2].child = grid[1][2]
    grid[1][2].child = sink
    assert not sink.is_on_new_segment()
    # Test sink with all parents
    grid[2][0].child = grid[2][1]
    grid[2][1].child = sink
    assert not sink.is_on_new_segment()


def test_is_on_new_segment_with_first_segment_returns_false():
    grid = Grid(((2, -1, -1), (-1, -1, -1), (1, -1, 0)))
    # Test first point on first segment
    grid[0][0].child = grid[0][1]
    assert not grid[0][1].is_on_new_segment()
    # Test second point on first segment
    grid[0][1].child = grid[0][2]
    assert not grid[0][2].is_on_new_segment()


def test_is_on_new_segment_with_new_segment_returns_true():
    grid = Grid(((2, -1, -1), (-1, -1, -1), (1, -1, 0)))
    point = grid[1][2]
    grid[0][0].child = grid[0][1]
    grid[0][1].child = grid[0][2]
    grid[0][2].child = point
    assert point.is_on_new_segment()


def test_is_on_new_segment_with_old_segment_returns_false():
    grid = Grid(((2, -1, -1), (-1, -1, -1), (1, -1, 0)))
    point = grid[2][1]
    grid[0][0].child = grid[0][1]
    grid[0][1].child = grid[1][1]
    grid[1][1].child = point
    assert not point.is_on_new_segment()
