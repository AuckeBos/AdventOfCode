import numpy as np
from aocd.models import Puzzle
from numpy import ndarray


class Line:
    def __init__(self, row: str):
        l, r = row.split(" -> ")
        self.x1, self.y1 = [int(v) for v in l.split(",")]
        self.x2, self.y2 = [int(v) for v in r.split(",")]

    @property
    def is_diagonal(self):
        return not self.is_horizontal and not self.is_vertical

    @property
    def is_horizontal(self):
        return self.y1 == self.y2

    @property
    def is_vertical(self):
        return self.x1 == self.x2

    @property
    def xs(self):
        if self.is_diagonal or self.is_horizontal:
            step = 1 if self.x2 > self.x1 else -1
            return list(range(self.x1, self.x2 + step, step))
        return [self.x1] * (abs(self.y1 - self.y2) + 1)

    @property
    def ys(self):
        if self.is_diagonal or self.is_vertical:
            step = 1 if self.y2 > self.y1 else -1
            return list(range(self.y1, self.y2 + step, step))
        return [self.y1] * (abs(self.x1 - self.x2) + 1)

    @property
    def points(self):
        return list(zip(self.xs, self.ys))


class Board:
    board: ndarray

    def __init__(self, size: int):
        self.board = np.full((size, size), 0, dtype=int)

    def tick(self, line: Line):
        for x, y in line.points:
            self.board[x, y] += 1

    @property
    def result(self):
        points = np.where(self.board > 1)
        count = len(points[0])
        return count


puzzle = Puzzle(year=2021, day=5)
lines = [Line(l) for l in puzzle.input_data.splitlines()]
board_a, board_b = Board(1000), Board(1000)
for line in lines:
    board_b.tick(line)
    if not line.is_diagonal:
        board_a.tick(line)

puzzle.answer_a = board_a.result
puzzle.answer_b = board_b.result
