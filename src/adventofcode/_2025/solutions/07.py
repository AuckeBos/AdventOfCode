from functools import lru_cache

import numpy as np

from adventofcode._templates.v20231204.puzzle_to_solve import PuzzleToSolve
from adventofcode.helpers.base_matrix import BaseMatrix, Directions, Position


class Puzzle7(PuzzleToSolve):
    matrix: BaseMatrix

    @property
    def day(self) -> int:
        return 7

    @property
    def year(self) -> int:
        return 2025

    @property
    def test_input(self) -> str:
        return """.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
..............."""

    @property
    def test_answer_a(self) -> int:
        return 21

    @property
    def test_answer_b(self) -> int:
        return 40

    @property
    def start(self) -> Position:
        start = np.where(self.matrix.data == "S")
        return Position(start[0][0], start[1][0])

    def parse_input(self, input_: str) -> BaseMatrix:
        self.matrix = BaseMatrix(input_, pad=None)
        return self.matrix

    def a(self, matrix: BaseMatrix) -> int:
        def iterate(pos: Position) -> int:
            if not matrix.is_in_bounds(pos):
                return 0  # At bottom. No splits in this path
            cell = matrix[pos]
            if cell == "|":
                return 0  # Already visited, do not double count
            elif cell == "^":
                # 1 split plus the splits from both sides
                return (
                    1
                    + iterate(pos + Directions.LEFT.value)
                    + iterate(pos + Directions.RIGHT.value)
                )
            elif cell == "." or cell == "S":
                matrix[pos] = "|"  # Mark as visited
                return iterate(pos + Directions.BOTTOM.value)
            else:
                raise ValueError(f"Unknown cell value {cell} at position {pos}")

        return iterate(self.start)

    def b(self, matrix: BaseMatrix) -> int:
        @lru_cache(maxsize=None)  # Prevent recomputation
        def iterate(pos: Position) -> int:
            if not matrix.is_in_bounds(pos):  # At bottom. 1 Path
                return 1
            if matrix[pos] == "^":  # sum both sides
                return iterate(pos + Directions.LEFT.value) + iterate(
                    pos + Directions.RIGHT.value
                )
            else:  # "." or "S", just go down
                return iterate(pos + Directions.BOTTOM.value)

        return iterate(self.start)


puzzle = Puzzle7()
puzzle.solve()
