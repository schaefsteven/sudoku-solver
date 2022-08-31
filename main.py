class Board():
    """Holds all of the cell objects."""
    def __init__(self):
        # Two-dimensional array of rows and columns. Indexed as
        # self.cells[row][column]
        self.cells = [[Cell(row, column) for column in range(9)] 
                for row in range(9)]

    def print(self):
        """Prints out the values of the board to command line."""
        row_count = 0
        column_count = 0
        for row in self.cells:
            if row_count % 3 == 0: 
                print("-" * 27)
            for cell in row:
                if column_count % 3 == 2:
                    end = "|"
                else:
                    end = " "
                print("{:2d}".format(cell.value), end = end)
                column_count += 1
            row_count += 1 
            print("")
        print("\n\n")

    def get(self, dimension, cell, attr="", exclude_self = False):
        """Returns information about the cells in the Board object

        dimension refers to a row, column, or square. 
        cell is the Cell object whose neighbors we are interested in.
        attr is the attribute of the cells that you wish to retrieve. If
        left blank, the method will return the Cell objects.
        """
        # Determine which cells are in the input cell's dimension
        # Row
        if dimension == "row":
            cells = self.cells[cell.row]
        # Column
        elif dimension in ("column", "col"):
            cells = [row[cell.column] for row in self.cells]
        # Square
        elif dimension in ("square", "sq"):
            start_row = (int(cell.row / 3) * 3)
            start_col = (int(cell.column / 3) * 3)
            # Grab the three rows that we want
            rows = self.cells[start_row : start_row + 3]
            # Build the cells array, must be one-dimensional
            cells = []
            for row in rows:
                for entry in row[start_col : start_col + 3]:
                    cells.append(entry) 
        # Invalid dimension argument handling
        else:
            raise NameError("Invalid dimension argument")
        # Remove the cell from cells if exclude_self is True
        if exclude_self:
            cells.remove(cell)
        return [getattr(value, attr, cell) for value in cells]
        
class Cell():
    """Contains info about each cell"""
    def __init__(self, row, column):
        # Possible values the cell could be
        self.possibilities = list(range(1, 10))
        # Solved value for cell. None if cell not solved. 
        self.value = None
        # Row that the cell is in
        self.row = row
        # Column that the cell is in
        self.column = column
    def __repr__(self):
        return f"Cell R:{self.row} C:{self.column}"

board = Board()
i = 0
for row in board.cells:
    for cell in row: 
        cell.value = i
        i += 1

board.print()
for row in board.cells:
    for cell in row:
        print(cell.row)
        print(board.get("row", cell, "value"))
        print(board.get("col", cell, "value"))
        print(board.get("sq", cell, "value"))
        print("-------")
