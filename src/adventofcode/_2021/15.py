from typing import List, Tuple

import numpy as np
from aocd.models import Puzzle
from numpy.typing import NDArray

from helpers import parse_matrix, neighbours


class Map:
    # For each node in map, set distance to start
    distances: NDArray
    # At each cell indicate the cost of entering that cell
    costs: NDArray
    # Boolean array. Value is true if cell is visited
    visited: NDArray
    # Current active node
    active_node: Tuple[int, int]
    # Min distance to current active node
    current_distance: int

    def __init__(self, matrix: NDArray, n_duplicate: int):
        """
        Upon create:
        - Create distance matrix of right shape, set distances to inf for non-start
        - Create weights dict, set weights to values of matrix
        """
        self.build_matrix(matrix, n_duplicate)
        self.distances = np.full(
            self.costs.shape, fill_value=np.iinfo(int).max, dtype=int
        )
        self.visited = np.full(self.costs.shape, fill_value=False, dtype=bool)
        self.distances[0, 0] = 0
        self.active_node = 0, 0

    def build_matrix(self, original: NDArray, n_duplicate: int):
        """
        Build matrix by duplicating the original matrix n_duplicate tiemes
        :param original:
        :param n_duplicate:
        :return:
        """
        new = np.full(
            (original.shape[0] * n_duplicate, original.shape[1] * n_duplicate),
            fill_value=0,
            dtype=int,
        )
        orig_r, orig_c = original.shape
        for r in range(n_duplicate):
            for c in range(n_duplicate):
                new_sub = original + r + c
                new_sub[new_sub > 9] = new_sub[new_sub > 9] % 9
                new[
                    orig_r * r : orig_r * (r + 1), orig_c * c : orig_c * (c + 1)
                ] = new_sub
        self.costs = new

    @property
    def end(self) -> Tuple[int, int]:
        return self.distances.shape[0] - 1, self.distances.shape[1] - 1

    def next(self):
        """
        Get next activen node, namely the one with least distance
        :return: r,c
        """
        distances = self.distances.copy()
        # Ensure visited nodes are not the next
        distances[self.visited] = np.iinfo(int).max
        res = np.argwhere(distances == np.min(distances))[-1]
        return res[0], res[1]

    def done(self) -> bool:
        """
        Done if destination is visited
        :return: bool
        """
        return self.visited[self.end]

    def get_neighbours(self) -> List[Tuple[int, int]]:
        result = neighbours(self.costs, *self.active_node, False)
        # Drop visited n
        result = [(r, c) for r, c in result if not self.visited[r, c]]
        return result

    def dijkstra(self) -> int:
        while not self.done():
            self._dijkstra()
        return self.distances[self.end]

    def _dijkstra(self):
        self.current_distance = self.distances[self.active_node]
        self.visited[self.active_node] = True
        n = self.get_neighbours()
        for r, c in n:
            # Set distance to neighbour
            self.distances[r, c] = min(
                self.costs[r, c] + self.current_distance, self.distances[r, c]
            )
        self.active_node = self.next()


puzzle = Puzzle(year=2021, day=15)
matrix = parse_matrix(puzzle.input_data, True)
puzzle.answer_a = Map(matrix, 1).dijkstra()
# Todo: Smarter solution
puzzle.answer_b = Map(matrix, 5).dijkstra()
