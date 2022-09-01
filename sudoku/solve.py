"""This module provides all of the tools for solving a sudoku board

Expects input in the form of a Board object from the data module in this
package. 
"""

def solve(board):
    """Executes the process of solving the board."""
    board = eliminate(board)
    while not check(board):
        board, change_made = unique(board)
        if not change_made:
            break
    return board


def eliminate(board):
    """If a cell has a value, eliminate that value from the neighbors' 
    possibilities lists"""
    for cell in board.all_cells:
        if cell.value:
            cell_eliminate(board, cell)
    return check_for_solved_cells(board)

def unique(board):
    """If a cell has a possibility that doesn't exist anywhere else in a 
    dimension, set the value to that unique possibility."""
    change_made = False
    for cell in board.all_cells:
        for dimen in ["row", "col", "sq"]:
            neighbor_possibilities = board.get(dimen, cell, "possibilities",
                    exclude_self = True)
            for poss in cell.possibilities:
                if poss not in neighbor_possibilities:
                    cell.value = poss
                    cell.possibilities = []
                    board = cell_eliminate(board,cell)
                    change_made = True
    return board, change_made

def cell_eliminate(board, cell):
    """Eliminate the value of a cell from the possibilies neighboring cells in 
    all dimensions"""
    for dimen in ["row", "col", "sq"]:
        for neighbor in board.get(dimen, cell):
            if cell.value in neighbor.possibilities:
                neighbor.possibilities.remove(cell.value)
    return board


def check(board):
    """Checks if the board has been solved"""
    # If any cell doesn't have a value, return False
    for cell in board.all_cells:
        if cell.value == None:
            return False
    # Else return True
    return True

def check_for_solved_cells(board):
    """Checks if any cells have only one possibility, if so, sets the value to 
    the only remaining possibility"""
    for cell in board.all_cells:
        if len(cell.possibilities) == 1:
            cell.value = cell.possibilities.pop()
    return board
