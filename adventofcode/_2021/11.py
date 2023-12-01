from itertools import combinations, permutations, product
from typing import List

import numpy as np
from aocd.models import Puzzle
from numpy.typing import NDArray


class Point:
    """
    A matrix consists of points. A point has a value, position, and neighbours
    """

    # List of neighbouring points.
    neighbours: List["Point"]
    # Raw val
    val: int
    # Row index
    r: int
    # Col index
    c: int
    # Used when iterating. Set to true when we have flashed, to prevent flashing more
    # than once
    marked: bool = False

    def __init__(self, r, c, val):
        self.r = r
        self.c = c
        self.val = val

    def save_neighbors(self, matrix):
        """
        Get the neighbours of the matrix, save them
        """
        results = []
        for ri, ci in product([-1, 0, 1], [-1, 0, 1]):
            r = self.r + ri
            c = self.c + ci
            if self._valid(matrix, r, c):
                results.append(matrix.points[r, c])
        self.neighbours = results

    # Check index bounds for neighbours
    def _valid(self, matrix, r, c) -> bool:
        return (
            not (r == self.r and c == self.c)
            and 0 <= r < matrix.points.shape[0]
            and 0 <= c < matrix.points.shape[1]
        )

    def __eq__(self, other):
        return self.r == other.r and self.c == other.c

    def tick(self):
        self.val += 1

    def flash(self):
        # Don't flash if yet flashed or val not > 9
        if self.marked or self.val <= 9:
            return
        self.marked = True
        for point in self.neighbours:
            point.tick()
            point.flash()

    def unmark(self) -> bool:
        """
        If was marked, unmark and set val to 0
        :return:  True if was marked
        """
        if self.marked:
            self.val = 0
            self.marked = False
            return True
        return False


class Matrix:
    # Matrix of values, but values are Point() objects
    points: NDArray

    def __init__(self, raw: NDArray):
        """
        Upon create: Save raw, save matrix of points. After all points have been
        created, save the neighbour points in the points itself
        :param raw: (n,m) points matrix
        """
        self.points = np.full(raw.shape, np.nan, dtype=object)
        for r in range(raw.shape[0]):
            for c in range(raw.shape[1]):
                self.points[r, c] = Point(r, c, raw[r, c])
        for r in range(raw.shape[0]):
            for c in range(raw.shape[1]):
                self.points[r, c].save_neighbors(self)

    def iterate_once(self):
        """
        Iterate all points once, eg:
        - Tick each point
        - Flash each point, if it must be flashed. Point will flash its neighbours
        - Unmark each flashed point
        :return: Number of flashed points
        """
        points = self.points.flatten()
        for point in points:
            point.tick()
        for point in points:
            point.flash()
        return sum(point.unmark() for point in points)

    def iterate(self, n: int):
        """
        Iterate n times, return total flash count
        """
        return sum([self.iterate_once() for _ in range(n)])

    def find_all_flash_iter(self):
        """
        Iterate once until we flash all octopuses in on iteration
        :return: The iteration at which this occurs
        """
        i = 0
        while True:
            i += 1
            if self.iterate_once() == np.prod(self.points.shape):
                return i


puzzle = Puzzle(year=2021, day=11)
lines = puzzle.input_data.splitlines()
raw_matrix = np.array([[int(v) for v in line] for line in lines])
matrix = Matrix(raw_matrix)
puzzle.answer_a = matrix.iterate(100)
matrix = Matrix(raw_matrix)
puzzle.answer_b = matrix.find_all_flash_iter()
