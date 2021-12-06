from helpers import read_input
from line import Line
from board import Board

rows = read_input("input", as_int=False)
lines = [Line(row) for row in rows]

PART = 1
allow_horizontal = PART == 2

board = Board(1000)
for line in lines:
    board.tick(line, allow_horizontal)
board.result()
