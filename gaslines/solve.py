def get_head(grid):
    """
    Returns any head point on the grid if at least one exists, otherwise None.

    Implementation-wise, this method searches for heads from right to left and top to
    bottom.
    """
    for row in grid:
        for point in row:
            if point.is_head():
                return point
    return None


def has_head(grid):
    return get_head(grid) is not None
