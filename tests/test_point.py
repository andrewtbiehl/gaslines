import pytest
from gaslines.point import Point


@pytest.mark.parametrize("grid", (None, [[0, 1], [None, None]], ((0, 1), (None, None))))
def test_grid_returns_grid_when_asked(grid):
    point = Point(grid, None)
    assert point.grid == grid


@pytest.mark.parametrize("location", (None, [0, 1], (0, 1)))
def test_location_returns_location_when_asked(location):
    point = Point(None, location)
    assert point.location == location


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
