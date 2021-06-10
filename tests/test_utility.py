"""All unit tests for the gaslines utility module."""


import pytest

from gaslines.utility import Direction, Observable, get_number_of_rows


GRID_STRING = """\
3   ·   ·
         \n\
·   2   ·
         \n\
*   ·   ·\
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


class Switch:
    """
    A simple class that initializes a boolean value to False and then, whenever
    directed, negates that value.
    """

    def __init__(self):
        self._state = False

    def flip(self):
        """Negates the current state."""
        self._state = not self._state

    @property
    def state(self):
        """Returns the current state."""
        return self._state


class MockDerivedObservable(Observable):
    """A mock class used to test inheritance of the Observable class."""

    # Mock __init__ method used to verify that Observables may have attributes
    def __init__(self, value):
        self.value = value

    @Observable.observe
    def mock_observed_method(self):
        """A mock method used to test the `observe` decorator functionality."""


def test_direction_returns_valid_direction():
    """Verifies that the Direction enum stores the correct direction vectors."""
    assert Direction.NORTH.value == (-1, 0)
    assert Direction.EAST.value == (0, 1)
    assert Direction.SOUTH.value == (1, 0)
    assert Direction.WEST.value == (0, -1)


def test_list_returns_expected_direction_order():
    """Verifies that listing the Direction elements returns the expected order."""
    assert list(Direction) == [
        Direction.NORTH,
        Direction.EAST,
        Direction.SOUTH,
        Direction.WEST,
    ]


@pytest.mark.parametrize(
    ("input_string", "expected_number"),
    (("", 1), ("a", 1), ("\n", 2), ("a\nb\nc", 3), (GRID_STRING, 5)),
)
def test_get_number_of_rows_with_input_string_returns_expected_number(
    input_string,
    expected_number,
):
    """Verifies that `get_number_of_rows` returns the expected number of rows."""
    assert get_number_of_rows(input_string) == expected_number


@pytest.mark.parametrize(
    ("observable", "method"),
    (
        (Observable(), Observable.notify),
        (MockDerivedObservable(None), MockDerivedObservable.notify),
        (MockDerivedObservable(None), MockDerivedObservable.mock_observed_method),
    ),
)
def test_observable_method_with_observers_notifies_observers(observable, method):
    """Verifies that Observable instances can register and notify observers."""
    # Instantiate two different example observers
    incrementor = Incrementor()
    switch = Switch()
    # Register (some methods of) these observers with the observable
    for observer in (incrementor.increment, switch.flip):
        observable.register(observer)
    # Notify the observers (directly or indirectly) an arbitrary number of times
    # Verify that the observers react as expected to being notified
    assert incrementor.count == 0
    assert not switch.state
    for i in range(1, 4):
        old_state = switch.state
        # Call the given method with respect to the given observable
        method(observable)
        assert incrementor.count == i
        assert switch.state == (not old_state)
