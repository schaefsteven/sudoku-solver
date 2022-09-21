"""This module provides all of the tools to create a sudoku board and 
manipulate its data. 
"""

import csv
import itertools
import copy

DIMENSIONS = ("row", "column", "square")
POSSIBILITIES = list(range(1,10))

class Board():
    """Holds all of the cell objects.

    If a csv file is passed, it will initialize the board to use those values.
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
        solving methods rely on the previous ones in order to be accurate."""
        change_made = True
        while change_made:
            change_made = False
            for cell in self.all_cells:
                change_made = cell.eliminate(self) or change_made
                change_made = cell.unique(self) or change_made
                change_made = cell.subset(self) or change_made
        # self.brute_force()
        return

    def brute_force(self):
        """If the solving algorithms cannot solve the puzzle, use the remaining
        possibilities to make guesses and check if that solves the puzzle.
        What we need to do: 
        find the first cell that doesn't have a value 
        choose the first poss 
        mark it as the origin_guess
        try to solve
        if it can't solve, it will call this method again 
        the cell we already guessed on will be skipped because it now has a 
        value. 
        if a cell has no value and no possibilities, break 
        we should never get here, but if all of the cells are filled but the 
        board is not solved, break. Raise exception? 
        
        Maybe instead of looping through the cells, first build a list of tuples 
        with the possibility and its parent cell. 
        How best to structure this? Could make an object instead of a tuple. 

        
        """
        # Create a copy of the board to make a guess with it without destroying
        # the info we have for the board
        bf_board = copy.deepcopy(self)
        all_poss = []
        
        class PossWrapper():
            """simple class to store a possibility value and its cell's index"""
            def __init__(self, poss, cell_index):
                self.poss = poss
                # Index of cell in all_cells list
                self.cell_index = cell_index

        # Populate the all_poss list
        for index, cell in enumerate(bf_board.all_cells):
            if not cell.value:
                for poss in cell.possibilities:
                    all_poss.append(PossWrapper(poss, index))

        # Main loop of this method
        for poss_wrapper in all_poss:
            # Set the cell to the current possibility
            bf_board.all_cells[poss_wrapper.cell_index] = poss_wrapper.poss
            # Try to solve the board (may recursively call this method)
            bf_board.solve()
            # If the board is now solved, set values in self to the solutions
            if bf_board.check():
                print("Brute force worked")
                for cell, bf_cell in zip(self.all_cells, bf_board.all_cells):
                    cell.set_value(bf_cell.value)
                return 
            # If the board is not solved, reset the bf_board to the known values
            # in the self. 
            else:
                bf_board = copy.deepcopy(self)

        print("Brute force didn't work.")


    def check(self):
        """Checks if the puzzle is solved correctly and prints out the 
        conclusion."""
        def check_dimen(dimen):
            for value in range(1, len(dimen)+1):
                if value not in dimen:
                    print("Error. Board not solved.")
                    return False
            return True
        # For each dimension, check all the row/col/sq in that dimen
        for dimen_type in (self.rows, self.columns, self.squares):
            for dimen in dimen_type:
                if not check_dimen([x.value for x in dimen]):
                    return False
        print("Board checked, no errors!")
        return True


class Cell():
    """Contains info about each cell"""
    def __init__(self, row, column, square):
        # Possible values the cell could be
        self.possibilities = POSSIBILITIES
        # Solved value for cell. None if cell not solved. 
        self.value = None
        # Row that the cell is in
        self.row = row
        # Column that the cell is in
        self.column = column
        # Square that the cell is in
        self.square = square

    def set_value(self,value):
        self.value = value
        self.possibilities = []

    def reset(self):
        self.value = None
        self.possibilities = POSSIBILITIES

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
                    self.check_if_solved()
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

    def check_if_solved(self):
        """Checks if there's only one possibility left and if so, sets the 
        value and possibilities of the cell accordingly"""
        if len(self.possibilities) == 1: 
            self.value = self.possibilities.pop()
        return

    def __repr__(self):
        return f"Cell R:{self.row} C:{self.column}"

