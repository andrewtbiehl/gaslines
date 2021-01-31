"""All unit tests for the gaslines point module."""


import pytest

from gaslines.grid import Grid
from gaslines.point import Point
from gaslines.utility import Direction


@pytest.mark.parametrize("grid", (None, [[0, 1], [None, None]], ((0, 1), (None, None))))
def test_grid_returns_grid_when_asked(grid):
    """Verifies that the grid property returns the expected grid."""
    point = Point(grid, None)
    assert point.grid == grid


@pytest.mark.parametrize("location", (None, [0, 1], (0, 1)))
def test_location_returns_location_when_asked(location):
    """Verifies that the location property returns the expected location."""
    point = Point(None, location)
    assert point.location == location


@pytest.mark.parametrize("row_index,column_index", ((0, 0), (0, 1), (1, 2)))
def test_indexes_return_correct_values_when_asked(row_index, column_index):
    """Verifies that the index properties return the expected indices."""
    point = Point(None, (row_index, column_index))
    assert point.row_index == row_index
    assert point.column_index == column_index


@pytest.mark.parametrize("type_", (1, 2, 3, 9, 45))
def test_is_source_returns_true_when_is_source(type_):
    """Verifies that `is_source()` returns true for a source point."""
    point = Point(None, None, type_)
    assert point.is_source()


@pytest.mark.parametrize("type_", (-1, 0, Point.PIPE, Point.SINK))
def test_is_source_returns_false_when_is_not_source(type_):
    """Verifies that `is_source()` returns false for a non-source point."""
    point = Point(None, None, type_)
    assert not point.is_source()


@pytest.mark.parametrize("type_", (0, Point.SINK))
def test_is_sink_returns_true_when_is_sink(type_):
    """Verifies that `is_sink()` returns true for a sink point."""
    point = Point(None, None, type_)
    assert point.is_sink()


@pytest.mark.parametrize("type_", (-1, 1, 2, 3, 9, 45, Point.PIPE))
def test_is_sink_returns_false_when_is_not_sink(type_):
    """Verifies that `is_sink()` returns false for a non-sink point."""
    point = Point(None, None, type_)
    assert not point.is_sink()


def test_init_sets_pipe_when_no_type_provided():
    """Verifies that the default init type is a pipe."""
    point = Point(None, None)
    assert not point.is_source()
    assert not point.is_sink()


def test_child_returns_child_when_provided_child():
    """Verifies that, with a child, the child property methods function correctly."""
    point = Point(None, None)
    child = Point(None, None)
    point.child = child
    assert point.has_child()
    assert point.child == child


def test_child_returns_no_child_when_not_provided_child():
    """Verifies that, with no child, the child property methods function correctly."""
    point = Point(None, None)
    assert not point.has_child()
    assert point.child is None


def test_child_returns_no_child_when_child_reset():
    """Verifies that resetting a point's child works as expected."""
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
    """Verifies that the neighbor method functions for a point with neighbors."""
    # The types have been carefully assigned for ease of testing
    grid = Grid(((0, 1, 0), (4, 5, 2), (0, 3, 0)))
    point = grid[1][1]
    neighbors = (grid[0][1], grid[1][2], grid[2][1], grid[1][0])
    # Test that the correct neighbor exists in each direction
    for i, direction in enumerate(Direction):
        assert point.has_neighbor(direction)
        neighbor = point.get_neighbor(direction)
        assert neighbor is neighbors[i]


def test_get_neighbor_with_missing_neighbor_returns_none():
    """Verifies that the neighbor method functions for nonexistent neighbors."""
    # The types have been carefully assigned for ease of testing
    grid = Grid(((1, 2, 0), (0, 0, 3), (0, 0, 4)))
    # Test the north west point
    point = grid[0][0]
    assert not (
        point.has_neighbor(Direction.NORTH) or point.has_neighbor(Direction.WEST)
    )
    assert point.get_neighbor(Direction.NORTH) is None
    # Test the north center point
    point = grid[0][1]
    assert not point.has_neighbor(Direction.NORTH)
    assert point.get_neighbor(Direction.NORTH) is None
    # Test the center east point
    point = grid[1][2]
    assert not point.has_neighbor(Direction.EAST)
    assert point.get_neighbor(Direction.EAST) is None
    # Test the south east point
    point = grid[2][2]
    assert not (
        point.has_neighbor(Direction.EAST) or point.has_neighbor(Direction.EAST)
    )
    assert point.get_neighbor(Direction.EAST) is None


def test_get_neighbors_with_some_neighbors_returns_correct_points():
    """Verifies that the neighbor method functions for points with some neighbors."""
    grid = Grid(((1, 2), (3, 0)))
    point = grid[0][0]
    expected_neighbors = (grid[0][1], grid[1][0])
    actual_neighbors = point.get_neighbors()
    assert len(expected_neighbors) == len(actual_neighbors) == 2
    for expected_neighbor, actual_neighbor in zip(expected_neighbors, actual_neighbors):
        assert expected_neighbor is actual_neighbor


def test_parent_with_parent_returns_correct_point():
    """Verifies that parent property methods function for a point with a parent."""
    grid = Grid(((2, -1), (1, 0)))
    parent, child = grid[0][0], grid[0][1]
    parent.child = child
    assert child.has_parent()
    assert child.parent is parent


def test_parent_with_no_parent_returns_none():
    """Verifies that parent property methods function for a point without a parent."""
    grid = Grid(((2, -1), (1, 0)))
    point = grid[0][1]
    assert not point.has_parent()
    assert point.parent is None


def test_parent_with_sink_returns_none():
    """Verifies that a sink point never reports that it has a parent."""
    grid = Grid(((2, -1), (1, 0)))
    source, pipe, sink = grid[0][0], grid[0][1], grid[1][1]
    source.child = pipe
    pipe.child = sink
    assert not sink.has_parent()
    assert sink.parent is None


def test_is_open_with_source_returns_false():
    """Verifies that a source point never reports that it is open."""
    grid = Grid(((2, -1), (1, 0)))
    assert not grid[0][0].is_open()


def test_is_open_with_sink_returns_true():
    """Verifies that a sink point always reports that it is open."""
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
    """Verifies that a pipe reports being open if and only if it's parentless."""
    grid = Grid(((2, -1), (1, 0)))
    pipe = grid[0][1]
    # Test pipe without parent is open
    assert pipe.is_open()
    # Test pipe with parent is not open
    grid[0][0].child = pipe
    assert not pipe.is_open()


def test_is_on_different_segment_with_source_returns_false():
    """
    Verifies that `is_on_different_segment` always reports false against sources.
    """
    grid = Grid(((2, -1, -1), (-1, -1, -1), (1, -1, 0)))
    source = grid[0][0]
    assert not grid[0][1].is_on_different_segment(source)
    assert not grid[1][0].is_on_different_segment(source)


def test_is_on_different_segment_with_same_segment_returns_true():
    """
    Verifies that `is_on_different_segment` is true for a point on a new segment.
    """
    grid = Grid(((2, -1, -1), (-1, -1, -1), (1, -1, 0)))
    grid[0][0].child = grid[0][1]
    assert grid[1][1].is_on_different_segment(grid[0][1])


def test_is_on_different_segment_with_different_segment_returns_false():
    """
    Verifies that `is_on_different_segment` is false for a point on the same segment.
    """
    grid = Grid(((2, -1, -1), (-1, -1, -1), (1, -1, 0)))
    grid[0][0].child = grid[0][1]
    assert not grid[0][2].is_on_different_segment(grid[0][1])


def test_remaining_segments_with_source_returns_type():
    """
    Verifies that the number of remaining segments of a source point is what was set.
    """
    grid = Grid(((3, -1, -1), (-1, 2, -1), (0, -1, -1)))
    assert grid[0][0].remaining_segments == 3
    assert grid[1][1].remaining_segments == 2


def test_remaining_segments_with_open_point_returns_none():
    """Verifies that the number of remaining segments of an open point is None."""
    grid = Grid(((3, -1, -1), (-1, 2, -1), (0, -1, -1)))
    assert grid[0][1].remaining_segments is None
    assert grid[1][0].remaining_segments is None
    assert grid[2][1].remaining_segments is None


def test_remaining_segments_with_sink_returns_none():
    """Verifies that the number of remaining segments of a sink is None."""
    grid = Grid(((3, -1, -1), (-1, 2, -1), (0, -1, -1)))
    assert grid[2][0].remaining_segments is None


def test_remaining_segments_with_first_segment_returns_no_change():
    """
    Verifies that a source's child has an unchanged number of remaining segments.
    """
    grid = Grid(((3, -1, -1), (-1, 2, -1), (0, -1, -1)))
    # Test first point on first segment
    grid[0][0].child = grid[0][1]
    assert grid[0][1].remaining_segments == 3
    # Test second point on first segment
    grid[0][1].child = grid[0][2]
    assert grid[0][2].remaining_segments == 3


def test_remaining_segments_with_new_segment_returns_change():
    """
    Verifies that moving to a new segment decrements the number of remaining segments.
    """
    grid = Grid(((3, -1, -1), (-1, 2, -1), (0, -1, -1)))
    # Test first point on second segment
    grid[0][0].child = grid[0][1]
    grid[0][1].child = grid[0][2]
    grid[0][2].child = grid[1][2]
    assert grid[1][2].remaining_segments == 2
    # Test second point on second segment has no change
    grid[1][2].child = grid[2][2]
    assert grid[2][2].remaining_segments == 2
    # Test first point on third segment
    grid[2][2].child = grid[2][1]
    assert grid[2][1].remaining_segments == 1


def test_has_relationship_with_no_relationship_returns_false():
    """Verifies that `has_relationship` returns false for two unrelated points."""
    grid = Grid(((3, -1, -1), (-1, 2, -1), (0, -1, -1)))
    for direction in Direction:
        assert not grid[1][1].has_relationship(direction)


def test_has_relationship_with_relationship_returns_true():
    """Verifies that `has_relationship` returns true for related points."""
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
    # Test north center pipe point
    assert grid[0][0].has_relationship(Direction.EAST)
    assert grid[0][1].has_relationship(Direction.WEST)
    assert grid[0][1].has_relationship(Direction.EAST)
    assert grid[0][2].has_relationship(Direction.WEST)
    # Test center center source point
    assert grid[1][1].has_relationship(Direction.WEST)
    assert grid[1][0].has_relationship(Direction.EAST)
    # Test south west sink point
    assert grid[1][0].has_relationship(Direction.SOUTH)
    assert grid[2][0].has_relationship(Direction.NORTH)
    assert grid[2][0].has_relationship(Direction.EAST)
    assert grid[2][1].has_relationship(Direction.WEST)


def test_has_relationship_with_no_neighbor_returns_false():
    """Verifies that `has_relationship` returns false against nonexistent points."""
    grid = Grid(((3, -1, -1), (-1, 2, -1), (0, -1, -1)))
    assert not grid[0][0].has_relationship(Direction.NORTH)
    assert not grid[0][0].has_relationship(Direction.WEST)
    assert not grid[0][1].has_relationship(Direction.NORTH)


def test_str_with_source_returns_type():
    """Verifies that the string value of a source point is its remaining segments."""
    grid = Grid(((3, -1, -1), (-1, 2, -1), (0, -1, -1)))
    assert str(grid[0][0]) == "3"
    assert str(grid[1][1]) == "2"


def test_str_with_pipe_returns_interpunct():
    """Verifies that the string value of a pipe point is the interpunct character."""
    grid = Grid(((3, -1, -1), (-1, 2, -1), (0, -1, -1)))
    for i, j in ((0, 1), (0, 2), (1, 2), (2, 1)):
        assert str(grid[i][j]) == chr(183) == "·"


def test_str_with_sink_returns_asterisk():
    """Verifies that the string value of a sink point is the asterisk character."""
    grid = Grid(((3, -1, -1), (-1, 2, -1), (0, -1, -1)))
    assert str(grid[2][0]) == "*"


def test_is_head_with_clean_puzzle_returns_sources():
    """Verifies that the heads of a completely unsolved puzzle are its sources."""
    grid = Grid(((3, -1, -1), (-1, 2, -1), (0, -1, -1)))
    sources_found = 0
    for row in grid:
        for point in row:
            if point.is_source():
                sources_found += 1
                assert point.is_head()
            else:
                assert not point.is_head()
    assert sources_found == 2


def test_is_head_with_head_pipe_returns_true():
    """Verifies that `is_head()` returns true for pipes that are currently heads."""
    grid = Grid(((3, -1, -1), (-1, 2, -1), (0, -1, -1)))
    grid[0][0].child = grid[0][1]
    assert not grid[0][0].is_head()
    assert grid[0][1].is_head()


def test_is_head_with_sink_returns_false():
    """Verifies that a sink never reports being a head."""
    grid = Grid(((3, -1, -1), (-1, 2, -1), (0, -1, -1)))
    # Test sink with no parents
    assert not grid[2][0].is_head()
    # Set path from "3"
    grid[0][0].child = grid[0][1]
    grid[0][1].child = grid[0][2]
    grid[0][2].child = grid[1][2]
    grid[1][2].child = grid[2][2]
    grid[2][2].child = grid[2][1]
    grid[2][1].child = grid[2][0]
    # Test sink with one parent
    assert not grid[2][0].is_head()
    # Set path from "2"
    grid[1][1].child = grid[1][0]
    grid[1][0].child = grid[2][0]
    # Test sink with all parents
    assert not grid[2][0].is_head()


def test_is_head_complete_puzzle_returns_no_heads():
    """Verifies that a completely solved puzzle has no remaining heads."""
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
    # Test that there are no heads anymore
    assert not [point for row in grid for point in row if point.is_head()]
