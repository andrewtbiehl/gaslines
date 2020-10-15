def print_and_backtrack(string):
    """
    On a standard terminal, clears everything below the cursor, prints the given
    string, and then returns the cursor to its prior location.
    """
    Cursor.clear_below()
    print(string)
    # Backtrack the cursor as many new lines as were printed
    number_of_lines = len(string.split("\n"))
    Cursor.move_up(number_of_lines)


class Cursor:
    """
    Static class that holds functions that wrap more complex interactions with a
    standard terminal.
    """

    # Credit to the blessings terminal library, the inspection of which helped with
    # the implementation of these methods

    @staticmethod
    def move_up(number_of_rows):
        """
        Moves the terminal cursor up from its current location the number of rows
        specified.

        Args:
            number_of_rows (int): The number of rows to move up. Negative values are
                ignored.
        """
        if number_of_rows > 0:
            # Prints a particular ANSI escape code for the desired outcome
            print(f"\x1b[{number_of_rows}A", end="")

    @staticmethod
    def clear_below():
        """
        Clears all rows below the cursor's current location (inclusive).
        """
        # Prints a particular ANSI escape code for the desired outcome
        print("\x1b[J", end="")
