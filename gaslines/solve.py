class Strategy:
    """
    Container class for algorithms that solve Gas Lines puzzles.

    It is recommended to call these strategies indirectly via the solve function.
    """

    # Note: These algorithms are implemented as instance methods in order to allow
    # the solve function to temporarily decorate them with additional features

    def full_recursive(self, grid, current=None):
        """
        A depth-first, fully recursive approach to solving Gas Lines puzzles.

        Mutates the grid object provided to search for a solution and returns True
        once a solution has been found or False if no solution exists.

        Retains a placeholder of its current position in order to be fully recursive.

        Args:
            grid (Grid): A partially solved Gas Lines grid.
            current (Point): A point in the grid from which to begin recursion. Should
                not be explicitly set with the initial call of the algorithm.

        Returns:
            bool: Whether the grid can be (or is) solved in its current state.
        """
        if current is None or current.is_sink():
            # Base case: a grid with no remaining heads is already in a solved state
            if not has_head(grid):
                return True
            current = get_head(grid)
        # Reset the child of "current" with the next candidate
        next_ = get_next(current)
        current.child = next_
        if next_ is None:
            return False
        # Recursive case: continue search starting at the child of "current" and then,
        # if no solution is found, search again starting at "current" with new child
        return self.full_recursive(grid, next_) or self.full_recursive(grid, current)

    def partial_recursive(self, grid):
        """
        A depth-first, partially recursive approach to solving Gas Lines puzzles.

        Mutates the grid object provided to search for a solution and returns True
        once a solution has been found or False if no solution exists.

        Recursive calls retain no memory of previous states, so the algorithm has to
        explicitly iterate through all recursive searches from the current state.

        Args:
            grid (Grid): A partially solved Gas Lines grid.

        Returns:
            bool: Whether the grid can be (or is) solved in its current state.
        """
        # Base case: a grid with no remaining heads is already in a solved state
        if not has_head(grid):
            return True
        current = get_head(grid)
        # Iterate through each possible next point from "current"
        while (next_ := get_next(current)) is not None:
            current.child = next_
            # Recursive case: continue searching with a new child of "current"
            if self.partial_recursive(grid):
                return True
        current.child = None
        return False


# Note: The solve function must appear below the Strategy class in the module in order
# to avoid a NameError


def solve(grid, strategy=Strategy.full_recursive):
    """
    Solves a Gas Lines puzzle (using the strategy provided).

    Mutates the grid object provided to search for a solution and returns True once a
    solution has been found or False if no solution exists.

    Args:
        grid (Grid): A (presumably unsolved) Gas Lines grid.
        strategy (Strategy class method): The choice of algorithm with which to solve
            the grid. Defaults to the "full_recursive" strategy.

    Returns:
        bool: Whether the grid has a solution.
    """
    strategy_name = strategy.__name__
    strategy_container = Strategy()
    solve = getattr(strategy_container, strategy_name)
    return solve(grid)


def get_next(current):
    """
    Returns a valid neighbor of "current", in the current recursive state, that has
    not yet been tried as its child, or None if all valid neighbors have been tried.
    """
    # Presumes that the order returned by get_neighbors is preserved over time
    neighbors = current.get_neighbors()
    # Get the index of the previously tested neighbor, the current child of "current"
    child_index = -1 if not current.has_child() else neighbors.index(current.child)
    # All untested neighbors occur strictly after the previously tested neighbor
    untested_neighbors = neighbors[child_index + 1 :]
    # Return the first of the untested neighbors that is worth considering
    for neighbor in untested_neighbors:
        if is_option(current, neighbor):
            return neighbor
    return None


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
