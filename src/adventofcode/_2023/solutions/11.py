from typing import List, Tuple

import numpy as np

from adventofcode._templates.v20231204.puzzle_to_solve import PuzzleToSolve
from adventofcode.helpers.base_matrix_v1 import BaseMatrixV1


class Map(BaseMatrixV1):
    """
    A map of galaxies
    """

    expansion_factor: int

    def set_expansion_factor(self, expansion_factor: int):
        """
        Set the expansion factor. This is the factor by which the empty rows and columns are expanded
        """
        self.expansion_factor = expansion_factor

    def get_expandabe_parts(self) -> Tuple[List[int], List[int]]:
        """
        Find the rows and columns that can be expanded (i.e. all have ".")
        """
        rows = [i for i in range(self.data.shape[0]) if (self.data[i, :] == ".").all()]
        cols = [i for i in range(self.data.shape[1]) if (self.data[:, i] == ".").all()]
        return rows, cols

    def find_galaxies(self) -> List[Tuple[int, int]]:
        """
        Find all galaxies (i.e. all positions with "#")
        """
        positions = np.where(self.data == "#")
        positions = list(zip(positions[0], positions[1]))
        return positions

    def find_length_sum(self) -> int:
        """
        Loop over all pairs of galaxies.
        For each galaxy, compute their distance in the unexpanded map.
        Then find the amount of expandable rows and columns between the two galaxies.
        Add the distance to the amount of expandable rows and columns times the expansion factor.
        Return the sum of all these distances
        """
        empty_rows, empty_cols = self.get_expandabe_parts()
        positions = self.find_galaxies()
        pairs = [
            (p1, p2) for p1 in positions for p2 in positions if p1 != p2 and p1 < p2
        ]
        distance_sum = 0
        for (r1, c1), (r2, c2) in pairs:
            # Find the expandable rows and cols that are between the two points
            amount_empty_rows_between = len(
                [r for r in empty_rows if min(r1, r2) < r < max(r1, r2)]
            )
            amount_empty_cols_between = len(
                [c for c in empty_cols if min(c1, c2) < c < max(c1, c2)]
            )
            # Distance without expansion applied
            unexpanded_distance = np.abs(r1 - r2) + np.abs(c1 - c2)
            # For each exapanable row/col, add expansion factor - 1 to the distance. -1 because one was already counted in the unexpanded distance
            expanded_distance = unexpanded_distance + (self.expansion_factor - 1) * (
                amount_empty_rows_between + amount_empty_cols_between
            )
            distance_sum += expanded_distance.sum()
        return distance_sum


class Puzzle11(PuzzleToSolve):
    @property
    def day(self) -> int:
        return 11

    @property
    def year(self) -> int:
        return 2023

    @property
    def test_input(self) -> str:
        return """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""

    @property
    def test_answer_a(self):
        return 374

    @property
    def test_answer_b(self):
        return 82000210

    def parse_input(self, input_: str):
        galaxy = Map()
        galaxy.parse_input(input_, pad=None)
        return galaxy

    def a(self, galaxy: Map):
        """
        Find the sum of all distances between galaxies, with expansion factor 2
        """
        galaxy.set_expansion_factor(2)
        return galaxy.find_length_sum()

    def b(self, galaxy: Map):
        """
        Find the sum of all distances between galaxies, with expansion factor 1000000
        """
        galaxy.set_expansion_factor(1000000)
        return galaxy.find_length_sum()


puzzle = Puzzle11()
puzzle.solve()
