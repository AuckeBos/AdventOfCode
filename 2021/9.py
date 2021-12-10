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
    # Used when getting basins. Set to true when we are running get_basin, to prevent
    # adding points more than once
    marked: bool = False

    def __init__(self, r, c, val):
        self.r = r
        self.c = c
        self.val = val

    def save_neighbors(self, matrix):
        """
        Get the neighbours of the matrix, save them
        """
        indices = [
            (self.r, self.c - 1),
            (self.r - 1, self.c),
            (self.r, self.c + 1),
            (self.r + 1, self.c),
        ]
        results = []
        for ri, ci in indices:
            if self._valid(matrix, ri, ci):
                results.append(matrix.points[ri, ci])
        self.neighbours = results

    # Check index bounds
    def _valid(self, matrix, r, c) -> bool:
        return 0 <= r < matrix.points.shape[0] and 0 <= c < matrix.points.shape[1]

    def __eq__(self, other):
        return self.r == other.r and self.c == other.c

    @property
    def is_low(self):
        return all([self.val < n.val for n in self.neighbours])

    @property
    def risk_level(self):
        return self.val + 1 if self.is_low else 0

    # Item may occur in basin if bnot 9, and not marked (eg yet added to basin)
    @property
    def may_occur_in_basin(self):
        return not self.marked and self.val != 9

    def get_basin(self) -> List["Point"]:
        self.marked = True
        basin = []
        for n in self.neighbours:
            if n.may_occur_in_basin:
                basin.extend(n.get_basin())
        basin.append(self)
        return basin


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

    # Flattened list of low points
    @property
    def low_points(self) -> List[Point]:
        return [p for p in self.points.flatten() if p.is_low]

    @property
    def risk_level(self):
        return sum([p.risk_level for p in self.low_points])

    @property
    def basin_len_sum(self) -> int:
        """
        Get The sum of the length of the 3 largest basins
        """
        basins = []
        for p in self.low_points:
            basins.append(p.get_basin())
        # Extract len, sort, multiply top 3
        result = np.prod(sorted([len(b) for b in basins], reverse=True)[:3])
        return result


puzzle = Puzzle(year=2021, day=9)
lines = puzzle.input_data.splitlines()
raw_matrix = np.array([[int(v) for v in line] for line in lines])
matrix = Matrix(raw_matrix)
puzzle.answer_a = matrix.risk_level
puzzle.answer_b = matrix.basin_len_sum
