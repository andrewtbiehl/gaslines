"""
Module that holds both general-purpose and gaslines-specific utilities used throughout
the gaslines test package.
"""


import itertools


def pairwise(iterable):
    """
    Returns an iterator of paired items, overlapping, from the original.

    This function is essentially identical to the function of the same name provided
    by the more-itertools project.

    Args:
        iterable (Iterable): The iterable of objects to pair up.

    Yields:
        tuple: The next ordered pair of items from the given iterable.
    """
    first, second = itertools.tee(iterable)
    next(second, None)
    yield from zip(first, second)
