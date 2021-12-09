from typing import List


class Point:
    # List of neighbouring points.
    neighbours: List["Point"]
    # Raw avl
    val: int
    # Raw row index
    r: int
    # Raw col index
    c: int
    # Used when getting basins. Set to true when we are runing get_basin, to prevent
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
