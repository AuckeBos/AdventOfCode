import numpy as np
from line import Line
from numpy import ndarray


class Board:
    board: ndarray

    def __init__(self, size:int):
        self.board = np.full((size, size), 0, dtype=int)

    def tick(self, line: Line, allow_diagonal= True):
        if line.is_diagonal() and not allow_diagonal:
            return
        for x,y in line.points():
            self.board[x, y] += 1

    def result(self):
        points = np.where(self.board > 1)
        count = len(points[0])
        print(count)
