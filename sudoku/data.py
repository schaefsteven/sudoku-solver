"""This module provides all of the tools to create a sudoku board and 
manipulate its data. 
"""

import csv
import itertools

class Board():
    """Holds all of the cell objects.

    If a csv file is passed, it will initialize the board to use those values.
    """
    def __init__(self, file = None):
        # Two-dimensional array of rows and columns. Indexed as
        # self.cells[row][column]
        self.cells = [[Cell(row, column) for column in range(9)] 
                for row in range(9)]

        # Creates an easy way to iterate over all of the cells at once
        self.all_cells = list(itertools.chain.from_iterable(self.cells))

        # Creates sets of the cells by dimension
        # Rows (redundant, but makes code more readable)
        self.rows = self.cells
        # Columns
        self.columns = [[row[col] for row in self.cells] 
                for col in len(self.cells[0])]
        # Squares
        
        self.squares 

        # Set values of cells to values from file if one is provided
        if file:
            with open(file) as csvfile:
                reader = csv.reader(csvfile, delimiter=',',)
                for cell, read_cell in zip(self.all_cells, next(reader)):
                    if read_cell != '0':
                        cell.value = int(read_cell)
                        cell.possibilities = []

    def print(self):
        """Prints out the values of the board to command line."""
        row_count = 0
        column_count = 0
        for row in self.cells:
            if row_count % 3 == 0: 
                print("-" * 18)
            for cell in row:
                if column_count % 3 == 2:
                    end = "|"
                else:
                    end = " "
                print_value = cell.value
                if not print_value:
                    print_value = 0
                print("{:1d}".format(print_value), end = end)
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
            cells = [x for x in cells if x.row != cell.row or x.column != 
                    cell.column]
        # Get the values
        values = [getattr(value, attr, value) for value in cells]
        # If values is multi-dimensional, make it one-dimensional.
        if hasattr(values[0], "__iter__"):
            values = list(itertools.chain.from_iterable(values))
        return values
    
    def solve(self):
        """Solves the puzzle"""
        change_made = True
        while change_made:
            change_made = False
            for cell in self.all_cells:
                change_made = cell.unique(self) or change_made
        return

    def check(self):
        """Checks if the puzzle is solved correctly and prints out the 
        conclusion."""
        def check_dimen(list):
            for value in range(1, len(list)+1):
                if value not in list:
                    return False
            return True
        # Rows
        for row in self.cells:
            if not check_dimen(row):
                return False
        # Columns
        for col in [row[col] for row in self.cells]:
            if not check_dimen(col):
                return False
        # Squares
        for sq in [self.get("sq", Cell(row, col) for row in 


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

    def unique(self, board):
        """First calls self.eliminate because this technique requires that
        the cell's possibilities list is up to date with known neighor values.
        Then checks if there is a possibility that is unique in any of the 
        cell's dimension. If so, set the value to that possibility and clear
        the possibilities list. Returns True if any changes were made to the 
        cell."""
        change_made = self.eliminate(board)
        for dimen in ("row", "col", "sq"):
            neighbor_possibilities = board.get(dimen, self, "possibilities",
                    exclude_self = True)
            for poss in self.possibilities:
                if poss not in neighbor_possibilities:
                    self.value = poss
                    self.possibilities = []
                    change_made = True
        return change_made

    def eliminate(self, board):
        """Removes values from self.possibilites if those values are known
        in any dimension. Returns True if any changes were made to the cell."""
        change_made = False
        for dimen in ("row", "col", "sq"):
            neighbor_values = board.get(dimen, self, "value")
            for n_val in neighbor_values:
                if n_val in self.possibilities:
                    self.possibilities.remove(n_val)
                    change_made = True
                    self.check_if_solved()
        return change_made

    def check_if_solved(self):
        """Checks if there's only one possibility left and if so, sets the 
        value and possibilities of the cell accordingly"""
        if len(self.possibilities) == 1: 
            self.value = self.possibilities.pop()
        return

    def __repr__(self):
        return f"Cell R:{self.row} C:{self.column}"

