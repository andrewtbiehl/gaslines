from gaslines.utility import Direction


class Point:
    """
    Represents a single lattice point in a Gas Lines puzzle grid
    """

    # Arbitrary integers used to represent "pipe" and "sink" type points
    # A point of type "source" is any point whose type value is positive
    PIPE = -1
    SINK = 0

    def __init__(self, grid, location, type_=PIPE):
        self._grid = grid
        self._location = location
        self._type = type_
        self._child = None

    @property
    def grid(self):
        return self._grid

    @property
    def location(self):
        return self._location

    def is_source(self):
        return self._type > 0

    def is_sink(self):
        return self._type == Point.SINK

    @property
    def child(self):
        return self._child

    @child.setter
    def child(self, point):
        self._child = point

    def has_child(self):
        return self.child is not None

    def get_neighbor(self, direction):
        """
        Returns the point adjacent to this one in the direction specified if one
        exists, otherwise None
        """
        # Get the hypothetical location of the neighbor
        # Pairwise add this point's location to the direction vector
        i, j = tuple(sum(vectors) for vectors in zip(self.location, direction.value))
        grid = self.grid
        # Get the neighbor only if that location is actually on the grid
        return grid[i][j] if 0 <= i < grid.height and 0 <= j < grid.length else None

    def has_neighbor(self, direction):
        return self.get_neighbor(direction) is not None

    def get_neighbors(self):
        """
        Returns all points that exist and are adjacent to this one, in the order
        specified by the Direction enum, skipping directions for which no such
        neighbor exists

        The specified Direction enum order is NORTH, EAST, SOUTH, WEST
        """
        return tuple(
            self.get_neighbor(direction)
            for direction in Direction
            if self.has_neighbor(direction)
        )

    @property
    def parent(self):
        """
        Returns the (necessarily adjacent) point with this as its child if such a
        point exists and if this is not a sink, otherwise None
        """
        # It doesn't make sense to request the parent of a sink
        if self.is_sink():
            return None
        for neighbor in self.get_neighbors():
            if neighbor.child is self:
                return neighbor
        return None

    def has_parent(self):
        return self.parent is not None
