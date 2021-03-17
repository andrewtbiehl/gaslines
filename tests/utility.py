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


def draw_path(grid, path):
    """
    Test helper function that "draws" the provided path on the provided grid.

    Args:
        grid (Grid): A Gas Lines grid.
        path (Iterable): A list of coordinates of points in the grid.
    """
    points = (grid[i][j] for i, j in path)
    for current_point, next_point in pairwise(points):
        current_point.child = next_point
