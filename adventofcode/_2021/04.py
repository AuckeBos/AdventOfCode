from typing import List, Tuple

import numpy as np
from aocd.models import Puzzle
from numpy import ndarray


class Board:
    BOARD_SIZE = 5

    # Last tick value
    last_tick = 0

    board: ndarray
    ticked: ndarray

    def __init__(self, numbers: List[int]):
        self.board = np.array(numbers).reshape(self.BOARD_SIZE, self.BOARD_SIZE)
        self.ticked = np.full((self.BOARD_SIZE, self.BOARD_SIZE), 0, dtype=bool)

    def tick(self, val: int):
        self.last_tick = val
        cell = np.where(self.board == val)
        # If cell is found
        if len(cell[0]):
            self.ticked[cell[0], cell[1]] = True
            if self.check():
                return self.score()
        return False

    def check(self):
        # True if any row or col has all tick
        colsums = np.all(self.ticked, axis=0)
        rowsums = np.all(self.ticked, axis=1)
        return np.any(colsums) or np.any(rowsums)

    def score(self):
        # Sum the not ticked values, multiply by last tick
        return np.sum(~self.ticked * self.board) * self.last_tick


def read_input(lines: List[str]) -> Tuple[List[int], List[Board]]:
    vals = [int(v) for v in lines.pop(0).split(",")]
    lines.pop(0)
    boards = []
    # Loop over each item in each row. But first: string and replace "  " with " "
    while lines:
        board = [
            int(item)
            for sublist in lines[:5]
            for item in sublist.strip().replace("  ", " ").split(" ")
        ]
        del lines[:6]
        boards.append(Board(board))
    return vals, boards


puzzle = Puzzle(year=2021, day=4)
lines = puzzle.input_data.splitlines()
vals, boards = read_input(lines)
bingos = []
for val in vals:
    for i, board in enumerate(boards):
        if i in bingos:
            continue
        score = board.tick(val)
        if score:
            if not puzzle.answered_a:  # PT1: stop on first
                puzzle.answer_a = score
            bingos.append(i)
            if not puzzle.answered_b and len(bingos) == len(boards):
                puzzle.answer_b = score
                exit()
