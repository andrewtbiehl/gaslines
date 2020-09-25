from gaslines.point import Point


class Grid:
    """
    Represents the grid of lattice points on which a Gas Lines puzzle takes place
    """

    def __init__(self, grid):
        self._grid = tuple(
            tuple(Point(self, (i, j), type_) for j, type_ in enumerate(row))
            for i, row in enumerate(grid)
        )
        self._height = len(self._grid)
        self._length = len(self._grid[0])

    def __getitem__(self, row_index):
        """
        Returns the row at the specified index of the grid
        """
        return self._grid[row_index]

    @property
    def height(self):
        return self._height

    @property
    def length(self):
        return self._length
