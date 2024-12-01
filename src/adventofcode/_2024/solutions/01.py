from collections import defaultdict
from typing import List

from adventofcode._templates.v20231204.puzzle_to_solve import PuzzleToSolve
from adventofcode.helpers.parsing import as_cols


class Puzzle1(PuzzleToSolve):
    @property
    def day(self) -> int:
        return 1

    @property
    def year(self) -> int:
        return 2024

    @property
    def test_input(self) -> str:
        return """3   4
4   3
2   5
1   3
3   9
3   3"""

    @property
    def test_answer_a(self):
        return 11

    @property
    def test_answer_b(self):
        return 31

    def parse_input(self, input_: str) -> List[List[int]]:
        """
        Parse input to cols. Sort the cols and return them.
        """
        l, r = as_cols(input_, sep="   ")
        return sorted(l), sorted(r)

    def a(self, input: List[List[int]]) -> int:
        """
        Sum the absolute differences between the two lists.
        """
        return sum(abs(x - y) for x, y in zip(*input))

    def b(self, input: List[List[int]]) -> int:
        """
        Create lookup for r. Then sum the product of the nums and their counts in r.
        """
        lookup = defaultdict(lambda: 0)
        for n in input[1]:
            lookup[n] += 1
        return sum(n * lookup[n] for n in input[0])


puzzle = Puzzle1()
puzzle.solve()
