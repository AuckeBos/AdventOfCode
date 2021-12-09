from typing import List

import numpy as np
from numpy.typing import NDArray

from point import Point


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
    def low_points(self) -> List[Point]:
        return [p for p in self.points.flatten() if p.is_low]

    def get_basin_len_sum(self) -> int:
        """
        Get The sum of the length of the 3 largest basins
        """
        basins = []
        for p in self.low_points():
            basins.append(p.get_basin())
        # Extract len, sort, multiply top 3
        result = np.prod(sorted([len(b) for b in basins], reverse=True)[:3])
        return result
