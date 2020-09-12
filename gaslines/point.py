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
