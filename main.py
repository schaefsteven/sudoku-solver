from sudoku import data, solve

def main():
    board = data.Board("sample_boards/board1.csv")
    board.print()
    board.solve()
    board.print()
    return

if __name__ == "__main__": 
    main()

