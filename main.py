class Cell():
    def __init__(self, value = None):
        self.possibilities = list(range(1, 10))
        self.value = value
        self.reported_initial_value = False

class Board():
    def __init__(self):
        # Two-dimensional array of rows and columns. Indexed as
        # self.cells[row][column]
        self.cells = [[Cell() for i in range(9)] for i in range(9)]

    def print(self):
        """ Prints out the values of the board to command line"""
        for row in self.cells:
            for cell in row:
                print(cell.value, end = " ")
            print("")

    def get_row(self, column, attr=""):
        cells = self.cells[row]
        return [getattr(cell, attr, cell) for cell in cells]

    def get_column(self, column, attr=""):
        cells = [row[column] for row in self.cells]
        return [getattr(cell, attr, cell) for cell in cells]

    def get_square(self, column, attr=""):
        cells = None
        return [getattr(cell, attr, cell) for cell in cells]

board = Board()
i = 0
for row in board.cells:
    for cell in row: 
        cell.value = i
        i += 1

board.print()

print(board.get_column(3, "value"))
print(board.get_column(3))
