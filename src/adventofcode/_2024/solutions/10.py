from collections import defaultdict

import numpy as np

from adventofcode._templates.v20231204.puzzle_to_solve import PuzzleToSolve
from adventofcode.helpers.base_matrix import BaseMatrix, Position


class Map(BaseMatrix):
    # set results in finding all peaks, list results in finding all paths to all peaks
    reachable_peaks: dict[Position, set[Position] | list[Position]]

    def __init__(self, input_: str):
        super().__init__(input_, None, int)

    def update_reachable_paths_for(
        self, current_position: Position, peak: Position
    ) -> None:
        """Update reachable_peaks. Add peak to paths of current_position.

        Do the same for all neighbors that are one step down, update those too.
        """
        if current_position != peak:
            # use 'add' or 'append', based on the type of reachable_peaks[current_position]
            self.reachable_peaks[current_position].add(peak) if isinstance(
                self.reachable_peaks[current_position], set
            ) else self.reachable_peaks[current_position].append(peak)
        for neighbor in self.adjacent_fields(
            current_position, include_axis=True, include_diagonal=False
        ):
            if self[neighbor] == self[current_position] - 1:
                self.update_reachable_paths_for(neighbor, peak)

    def update_reachable_paths(self) -> int:
        """For each peak, find all paths to the peak.

        Return the sum of the path count for all heads.
        """
        for peak in np.argwhere(self.data == 9):
            self.update_reachable_paths_for(Position(*peak), Position(*peak))
        return sum(
            len(self.reachable_peaks[Position(*trail_head)])
            for trail_head in np.argwhere(self.data == 0)
        )

    def score(self) -> int:
        """update_reachable_paths with set().

        This means that we only compute the reachable peaks from each start
        """
        self.reachable_peaks = defaultdict(lambda: set())
        return self.update_reachable_paths()

    def rate(self) -> int:
        """update_reachable_paths with list().

        This means that we compute all unique paths to all reachable peaks from each start
        """
        self.reachable_peaks = defaultdict(lambda: [])
        return self.update_reachable_paths()


class Puzzle10(PuzzleToSolve):
    @property
    def day(self) -> int:
        return 10

    @property
    def year(self) -> int:
        return 2024

    @property
    def test_input(self) -> str:
        return """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""

    @property
    def test_answer_a(self):
        return 36

    @property
    def test_answer_b(self):
        return 81

    def parse_input(self, input_: str) -> Map:
        return Map(input_)

    def a(self, map_: Map):
        return map_.score()

    def b(self, map_: Map):
        return map_.rate()


puzzle = Puzzle10()
puzzle.solve()
