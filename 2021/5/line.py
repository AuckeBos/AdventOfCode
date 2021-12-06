import math


class Line:

    def __init__(self, row: str):
        l,r = row.split(' -> ')
        self.x1, self.y1 = [int(v) for v in l.split(',')]
        self.x2, self.y2 = [int(v) for v in r.split(',')]

    def is_diagonal(self):
        return not self.is_horizontal() and not self.is_vertical()

    def is_horizontal(self):
        return self.y1 == self.y2

    def is_vertical(self):
        return self.x1 == self.x2

    def y_diff(self):
        return abs(self.y1 - self.y2) + 1

    def x_diff(self):
        return abs(self.x1 - self.x2) + 1

    def xs(self):
        if self.is_diagonal() or self.is_horizontal():
            step = 1 if self.x2 > self.x1 else -1
            return list(range(self.x1, self.x2 + step, step))
        return [self.x1] * self.y_diff()

    def ys(self):
        if self.is_diagonal() or self.is_vertical():
            step = 1 if self.y2 > self.y1 else -1
            return list(range(self.y1, self.y2 + step, step))
        return [self.y1] * self.x_diff()

    def points(self):
        return list(zip(self.xs(), self.ys()))