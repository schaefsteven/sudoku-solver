"""This module provides all of the tools to create a sudoku board, manipulate 
its data, and solve the puzzle.
"""

import csv
import itertools
import copy

DIMENSIONS = ("row", "column", "square")

class Board():
    """Holds all of the cell objects. If a csv file is passed, it will 
    initialize the board to use those values.
    """
    def __init__(self, file = None):
        # Two-dimensional array of rows and columns. Indexed as
        # self.cells[row][column]
        self.cells = [[Cell(row, column, None) for column in range(9)] 
                for row in range(9)]

        # Creates an easy way to iterate over all of the cells at once
        self.all_cells = list(itertools.chain.from_iterable(self.cells))

        # Creates sets of the cells by dimension
        # Rows (redundant, but makes code more readable)
        self.rows = self.cells
        # Columns
        self.columns = [[row[col] for row in self.cells] 
                for col in range(len(self.cells[0]))]
        # Squares
        self.squares = []
        square_index = 0
        # For each index_cell
        for index_row in self.rows[::3]:
            for index_cell in index_row[::3]:
                # Find our starting row and column
                start_row = (int(index_cell.row / 3) * 3)
                start_col = (int(index_cell.column / 3) * 3)
                # Grab the three rows that we want
                rows = self.cells[start_row : start_row + 3]
                # Build the cells array, must be one-dimensional
                cells = []
                for row in rows:
                    for entry in row[start_col : start_col + 3]:
                        cells.append(entry) 
                # Set the square attribute for each square
                for cell in cells:
                    cell.square = square_index
                square_index += 1
                # Append the cells array (our new square) to the squares array
                self.squares.append(cells)

        # Set values of cells to values from file if one is provided
        if file:
            with open(file) as csvfile:
                reader = csv.reader(csvfile, delimiter=',',)
                for cell, read_cell in zip(self.all_cells, next(reader)):
                    if read_cell != '0':
                        cell.value = int(read_cell)
                        cell.possibilities = []

        # Initialize the saved_cells array
        self.saved_cells = []

    def print(self):
        """Prints out the values of the board to command line. Used for 
        debugging.
        """
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
            cells = self.rows[cell.row]
        # Column
        elif dimension in ("column", "col"):
            cells = self.columns[cell.column]
        # Square
        elif dimension in ("square", "sq"):
            cells = self.squares[cell.square]

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
        """Solves the puzzle. The order of the method calls matters! Certain
        solving methods rely on the previous ones in order to be accurate.
        Returns bool indicating whether it was successful.
        """
        # Loop through all cells and run the three solving algos on them.
        change_made = True
        while change_made:
            change_made = False
            for cell in self.all_cells:
                change_made = cell.eliminate(self) or change_made
                change_made = cell.unique(self) or change_made
                change_made = cell.subset(self) or change_made
        if self.check():
            return True
        else:
            return self.brute_force()

    def brute_force(self):
        """If the solving algorithms cannot solve the puzzle, use the remaining
        possibilities to make guesses and check if that solves the puzzle.
        Returns bool indicating whether it was successful.
        """
        # If the board is already invalid, return False
        if not self.check_valid():
            return False
        guess_cell = None
        for cell in self.all_cells:
            if not cell.value:
                # This statement finds the first cell with no value
                if not guess_cell:
                    guess_cell = cell
                # If there are any empty cells with no poss, return False
                if len(cell.possibilities) <= 0: 
                    return False
        # If there are no empty cells, return False
        if not guess_cell:
            return False
        
        # Main loop for this method
        for poss in guess_cell.possibilities:
            # Create a save state so we can revert to it if we guess wrong.
            self._save_state()
            # Make a guess
            guess_cell.set_value(poss)
            # If board is solved, return True
            if self.solve():
                return True
            # If not, restore state of the board before we guessed. 
            self._restore_state()
        # If we reach this, there are no solutions to the current board, so 
        # we go back a step
        else:
            return False

    def check_valid(self):
        """Checks if any rules are broken and returns bool."""
        def check_dimen(dimen):
            for value in dimen:
                if value:
                    if dimen.count(value) > 1:
                        return False
            return True

        # For each dimension, check all the row/col/sq in that dimen
        for dimen_type in (self.rows, self.columns, self.squares):
            for dimen in dimen_type:
                if not check_dimen([x.value for x in dimen]):
                    return False
        return True

    def check(self):
        """Checks if the puzzle is solved correctly and returns bool."""
        def check_dimen(dimen):
            for value in range(1, len(dimen)+1):
                if value not in dimen:
                    return False
            return True

        # For each dimension, check all the row/col/sq in that dimen
        for dimen_type in (self.rows, self.columns, self.squares):
            for dimen in dimen_type:
                if not check_dimen([x.value for x in dimen]):
                    return False
        return True

    def _save_state(self):
        """Saves a list of the cells as they are so it can be recalled later"""
        self.saved_cells.append(copy.deepcopy(self.all_cells))

    def _restore_state(self):
        """Restores a state saved in the _save_state method"""
        for cell, saved_cell in zip(self.all_cells, self.saved_cells.pop()):
            cell.value = saved_cell.value
            cell.possibilities = saved_cell.possibilities

class Cell():
    """Contains info about each cell"""
    def __init__(self, row, column, square):
        # Possible values the cell could be
        self.possibilities = list(range(1, 10))
        # Solved value for cell. None if cell not solved. 
        self.value = None
        # Row/column/square that the cell is in
        self.row = row
        self.column = column
        self.square = square

    def __repr__(self):
        return f"Cell R:{self.row} C:{self.column}"

    def set_value(self,value):
        self.value = value
        self.possibilities = []

    def reset(self):
        self.value = None
        self.possibilities = list(range(1, 10))

    # Solving Algorithms: 
    def eliminate(self, board):
        """Removes values from self.possibilites if those values are known
        in any dimension. Returns True if any changes were made to the cell."""
        change_made = False
        # Do this in each dimension
        for dimen in DIMENSIONS:
            # Grab the list of known values in neighbor cells
            neighbor_values = board.get(dimen, self, "value")
            for n_val in neighbor_values:
                # Eliminate those values from self.poss
                if n_val in self.possibilities:
                    self.possibilities.remove(n_val)
                    change_made = True
        self._check_if_solved()
        return change_made

    def unique(self, board):
        """Checks if there is a possibility that is unique in any of the 
        cell's dimensions. If so, set the value to that possibility and clear
        the possibilities list. Returns True if any changes were made to the 
        cell. Must be run after self.eliminate because this technique requires 
        that the cell's possibilities list is up to date with known neighor 
        values."""
        change_made = False
        # Do this in each dimension
        for dimen in DIMENSIONS:
            # Grab the list of possibilities for all other cells in dimension
            neighbor_possibilities = board.get(dimen, self, "possibilities",
                    exclude_self = True)
            # Check for a unique value in self.poss
            for poss in self.possibilities:
                if poss not in neighbor_possibilities:
                    self.value = poss
                    self.possibilities = []
                    change_made = True
        return change_made

    def subset(self, board):
        """Checks if there are cells that have identical possibility lists. If
        the number of cells that share identical poss lists is the same as the 
        number of possibilities in those lists, then those possibilities can be 
        removed from all other cells in the dimension. Must be run after 
        self.eliminate"""
        change_made = False
        # Do this in each dimension
        for dimen in DIMENSIONS:
            # Keep track of matching neighbors, starts at one to count self. 
            matching_neighbors = 1
            # Loop through neighbors, excluding self.
            for neighbor in board.get(dimen, self, exclude_self = True):
                # Check if the poss lists match
                if neighbor.possibilities == self.possibilities:
                    matching_neighbors += 1
            # Check if the matching neighbors matches the number of possibilities
            if matching_neighbors == len(self.possibilities):
                # Loop through the neighbors
                for neighbor in board.get(dimen, self, exclude_self = True):
                    # Check if this cell is one of the matching neighbors.
                    if neighbor.possibilities != self.possibilities:
                        # Remove self.poss values from all other poss lists
                        # in this dimension
                        for poss in self.possibilities:
                            if poss in neighbor.possibilities:
                                change_made = True
                                neighbor.possibilities.remove(poss)
        return change_made

    def _check_if_solved(self):
        """Checks if there's only one possibility left and if so, sets the 
        value and possibilities of the cell accordingly"""
        if len(self.possibilities) == 1: 
            self.value = self.possibilities.pop()
        return

