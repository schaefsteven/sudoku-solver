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
