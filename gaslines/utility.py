"""
Module that holds miscellaneous, general-purpose utilities used throughout the
gaslines package.
"""


import functools
from enum import Enum


class Direction(Enum):
    """
    Two-dimensional vectors representing the four cardinal directions

    It is expected that the order listed here is preserved
    """

    NORTH = (-1, 0)
    EAST = (0, 1)
    SOUTH = (1, 0)
    WEST = (0, -1)


def get_number_of_rows(string):
    """
    Determines the number of rows (a.k.a. lines) contained in the given string. This
    is equivalent to counting one more than the number of newline characters in the
    string.

    Args:
        string (str): The string whose rows are to be counted.
    """
    return len(string.split("\n"))


class Observable:
    """
    A simple implementation of the observer design pattern.

    This class may be instantiated directly but also, more importantly, other classes
    can use its functionality out-of-the-box by specifying it as a base class.
    """

    def __new__(cls, *_args, **_kwargs):
        # The args and kwargs may be used by __init__ but are not used here
        instance = super().__new__(cls)
        # Explicitly initialize the list of observers
        # This is done here to prevent the need for explicit initialization elsewhere
        instance._observers = []
        return instance

    def register(self, observer):
        """
        Registers a callable as an 'observer' of this observable.

        Args:
            observer (callable): A callable to invoke upon notification by this
                observable.
        """
        self._observers.append(observer)

    def notify(self):
        """
        'Notifies' all previously registered observers.

        Under the current implementation, observers are notified exactly in accordance
        with the order and amount that they were registered.
        """
        for observer in self._observers:
            observer()

    @staticmethod
    def observe(method):
        """
        Decorates a given method so that observers are notified any time it is called,
        immediately afterwards.

        This method is intended to be used only as a decorater of methods of
        Observable-derived classes.

        Args:
            method (Observable class method): The method to observe.
        """

        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            result = method(self, *args, **kwargs)
            self.notify()
            return result

        return wrapper
