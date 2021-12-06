from numpy import ndarray
from typing import List
import numpy as np

class Board:
    BOARD_SIZE= 5

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
        return np.sum(~self.ticked*self.board)*self.last_tick