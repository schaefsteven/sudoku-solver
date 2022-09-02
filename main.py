from sudoku import data

def main():
    board = data.Board("sample_boards/board0.csv")
    board.print()
    board.solve()
    board.check()
    board.print()
    return

if __name__ == "__main__": 
    main()

