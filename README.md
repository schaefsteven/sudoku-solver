# Sudoku Solver

This is a program that can solve any valid sudoku puzzle. It is written in Python using the Kivy framework. It has a full GUI for ease of use.

Example of a puzzle entered into the app:

![sudoku solver with an unsolved puzzle](./readme-media/before-solve.PNG)

After clicking solve, if the app is able to solve the puzzle, it displays it like this:

![sudoku solver with a solved puzzle](./readme-media/after-solve.PNG)

The typical sudoku puzzle that you will find in a book or on a website has only one solution and this program will find it. However, it is possible to give the program a starting board that has multiple solutions. In this case, the program will stop at the first solution it finds and display it to you. Finally, it is possible to give the program a puzzle that does not have any solutions. In this case, the program will notify you that no solutions exist and leave the puzzle as you input it. 

![sudoku solver showing no-solutions message](./readme-media/no-solutions.PNG)


## Algorithms

This program uses a couple of different algorithms to solve the puzzle. 

### Elimination

If a cell's neighbors (cells in the same row, column, or square) have known values, we can eliminate those values from that cell's possibilities list. 

### Unique Possibility 

If a possibility occurs only once in any dimension (row, column, or square), then that must be the value for the cell that it is in. 

### Subsets

Typically referred to by the sudoku community as naked pairs/triplets/etc, if a group of neighbor cells all have the same possibilities and the number of possibilities is the same as the number of members of the group, then we know that those numbers must go into the cells of the group. We can therefore remove those possibilities from the rest of the neighbors not in the group.

### Backtracking Brute-Force

Most easy and medium difficulty puzzles and many hard difficulty puzzles can be solved with the above algorithms, but as the puzzles get harder, these algorithms are not enough to solve the entire puzzle. Rather than resort to more and more complex algorithms that may or may not lead us to the solution, we can brute-force our way to the answer. 

However, a simple brute-force approach to the problem is inefficient, so we instead use a backtracking algorithm that checks at each step to see if the current state of the board is valid, and if not, it stops searching that branch of the tree. 

The backtracking algorithm is able to solve any puzzle on its own without the previous algorithms, but using the above algorithms, we are able to reduce the size of the problem much more quickly, so we use the first three algorithms until they fail, and only then do we start brute-forcing the answer. 

## Installation

### For Users

If you just want to download and use the program, you can download the latest release by [clicking here](https://github.com/schaefsteven/sudoku_solver/releases/download/Sudoku/SudokuSolver.exe).

**IMPORTANT**: The first time you download the program, Windows Defender will warn you that the app is unrecognized. Simply click "More info" which will reveal a button labeled "Run Anyway." Click that button and the program will then run. 

### For Developers
It is recommended to install with Pipenv. You need to have [Python 3.x](https://wiki.python.org/moin/BeginnersGuide/Download) and [Pipenv](https://pypi.org/project/pipenv/) installed first.
```
git clone https://github.com/schaefsteven/sudoku_solver.git
cd .\sudoku_solver\
pipenv install
```
You can then run the program with:
```
pipenv run main.py
```
