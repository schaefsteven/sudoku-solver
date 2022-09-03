from sudoku import sudoku

def main():
    board = sudoku.Board("sample_boards/board2.csv")
    board.print()
    board.solve()
    board.check()
    board.print()
    return

if __name__ == "__main__": 
    main()

