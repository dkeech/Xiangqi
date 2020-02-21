# Author: Dan Keech
# Date: 2/20/2020
# CS 162 Final Project
# This file defines the Xiangqi board

class Board:
    def __init__(self):
        self._rows = 10
        self._cols = 9
        self.rows = [['R', 'K', 'E', 'A', 'G', 'A', 'E', 'K', 'R'],
                     [0 for x in range(9)],
                     [0, 'C', 0, 0, 0, 0, 0, 'C', 0],
                     ['P', 0, 'P', 0, 'P', 0, 'P', 0, 'P'],
                     [0 for x in range(9)],
                     [0 for x in range(9)],
                     ['p', 0, 'p', 0, 'p', 0, 'p', 0, 'p'],
                     [0, 'c', 0, 0, 0, 0, 0, 'c', 0],
                     [0 for x in range(9)],
                     ['r', 'k', 'e', 'a', 'g', 'a', 'e', 'k', 'r']]

    def move_piece(self, name, from_row, from_col, to_row, to_col):
        self.rows[to_row][to_col] = name
        print(self.rows[from_row][from_col])
        self.rows[from_row][from_col] = 0


    def __repr__(self):
        count = 0
        print(" ", end="")
        for i in range(self._cols):
            print(str(i), end="---")
        print("\n")
        for i in self.rows:
            print(count, end="")
            for x in i:
                if x is 0:
                    print("+---", end="")
                else:
                    print(f"{x}---", end="")
            count += 1
            print("\n |   |   |   |   |   |   |   |   |")

    def empty_board(self):
        for i in range(self._rows-1, 0, -1):
            print(str(i) + "+---" * (self._cols-1) + "+")
            print(" ", end="")
            print("|   " * self._cols)
        print(" ", end="")
        print("+---" * (self._cols-1) + "+")
        print(" ", end="")
        for i in range(self._cols):
            print(str(i), end="   ")


board = Board()
# board.empty_board()
print(board.__repr__())
board.move_piece('C', 2, 1, 9, 1)
print(board.__repr__())
# board.check_indices()