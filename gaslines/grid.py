"""
Container module for the gaslines Grid class, which holds grid-specific data for a Gas
Lines puzzle.
"""


from gaslines.point import Point
from gaslines.utility import Direction


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
        """Returns the height (i.e., number of rows) of the grid."""
        return self._height

    @property
    def length(self):
        """Returns the length (i.e., number of columns) of the grid."""
        return self._length

    def __str__(self):
        """
        Returns a Unicode representation of the grid in its current state
        """
        lines = []
        for row in self:
            row_relationships, column_relationships = [], []
            for point in row:
                # Add a representation of the point and its eastern relationship
                row_relationships.append(str(point))
                row_relationships.append(Grid._get_row_relationship(point))
                # Add a representation of the point's southern relationship
                column_relationships.append(Grid._get_column_relationship(point))
            # Concatenate row_relationships, discarding the excess row_relationship
            lines.append("".join(row_relationships[:-1]))
            # Concatenate column_relationships
            lines.append("   ".join(column_relationships))
        # Concatenate all lines, discarding the excess column_relationship
        return "\n".join(lines[:-1])

    @staticmethod
    def _get_row_relationship(point):
        """
        Helper method that returns a Unicode representation of a point's eastern
        relationship
        """
        return "---" if point.has_relationship(Direction.EAST) else "   "

    @staticmethod
    def _get_column_relationship(point):
        """
        Helper method that returns a Unicode representation of a point's southern
        relationship
        """
        return "|" if point.has_relationship(Direction.SOUTH) else " "
