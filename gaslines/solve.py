def is_option(current, neighbor):
    """
    Returns whether the neighbor is a valid option to be set as the child of current.
    """
    # Remaining segments that the neighbor would have as the child of current
    neighbor_remaining_segments = (
        current.remaining_segments - neighbor.is_on_different_segment(current)
    )
    return (
        neighbor.is_open()
        and neighbor_remaining_segments > 0
        # Logically equivalent to "neighbor is sink implies one remaining segment"
        and (not neighbor.is_sink() or neighbor_remaining_segments == 1)
    )


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
