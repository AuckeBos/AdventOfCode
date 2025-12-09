import itertools

from adventofcode._templates.v20231204.puzzle_to_solve import PuzzleToSolve
from adventofcode.helpers.base_matrix import Position


class Puzzle9(PuzzleToSolve):
    @property
    def day(self) -> int:
        return 9

    @property
    def year(self) -> int:
        return 2025

    @property
    def test_input(self) -> str:
        return """7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3"""

    @property
    def test_answer_a(self) -> int:
        return 50

    @property
    def test_answer_b(self) -> int:
        return -1

    def parse_input(self, input_: str) -> list[Position]:
        return [
            Position(*map(int, line.split(","))) for line in input_.strip().splitlines()
        ]

    def a(self, tiles: list[Position]) -> int:
        return max(
            (abs(pos1.i - pos2.i) + 1) * (abs(pos1.j - pos2.j) + 1)
            for pos1, pos2 in itertools.combinations(tiles, 2)
        )

    def b(self, tiles: list[Position]) -> int:
        return 0


puzzle = Puzzle9()
puzzle.solve()
