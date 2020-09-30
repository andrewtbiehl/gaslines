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

    @property
    def row_index(self):
        return self.location[0]

    @property
    def column_index(self):
        return self.location[1]

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

    def has_relationship(self, direction):
        """
        Returns whether this is related to the adjacent point in the direction
        specified

        No relationship (False) includes a situation where the adjacent point does not
        exist
        """
        if not self.has_neighbor(direction):
            return False
        neighbor = self.get_neighbor(direction)
        # Note: we cannot use self.parent here because sinks may have multiple parents
        return self.child is neighbor or neighbor.child is self

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

    def is_open(self):
        """
        Returns whether or not this is open to be set as a child of another point

        Sink points always display as open
        """
        return not self.is_source() and not self.has_parent()

    def is_head(self):
        """
        Returns whether this is the current "head" of a path from source to sink

        Sink nodes are not considered heads so a complete path from source to sink is
        headless. As a consequence of this, a completed puzzle has no heads.
        """
        return not self.is_open() and not self.has_child()

    def is_on_different_segment(self, neighbor):
        """
        Determines whether this is on a different straight line segment from the given
        neighbor, along the directed path from source to sink

        Correct usage of this method presupposes that the neighbor provided either
        has a single parent or is a source point

        The child of a source point is not considered to be on a different segment
        from its parent, even though its parent is not preceded by a segment
        """
        # The first segment after a source point is considered a "freebie"
        # Non-source neighbors without parents are irrelevant
        if not neighbor.has_parent():
            return False
        # Check whether this is in a different row from the parent of its neighbor
        # Use of row over column was an arbitrary decision
        return abs(neighbor.parent.row_index - self.row_index) == 1

    @property
    def remaining_segments(self):
        """
        Returns the exact number of remaining straight line segments required to
        connect this point to a sink
        """
        # It doesn't make sense to request the remaining segments of an open point
        if self.is_open():
            return None
        # Base case: number of remaining segments is fixed if the point is a source
        if self.is_source():
            return self._type
        # Recursive case: remaining segments of parent, minus one if on new segment
        parent = self.parent
        return parent.remaining_segments - self.is_on_different_segment(parent)

    def __str__(self):
        """
        Returns a single Unicode character representation of the (type of) point

        For sources, this character is a digit, representing the number of remaining
        segments to connect that point to a sink
        """
        if self.is_sink():
            return "*"
        if self.is_source():
            return str(self.remaining_segments)
        # For pipe points, return the interpunct character, "·"
        return chr(183)
