from collections import defaultdict
from typing import List, Tuple

from adventofcode._templates.v20231204.puzzle_to_solve import PuzzleToSolve


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

    def parse_input(self, input_: str) -> Tuple[List[int], List[int]]:
        l, r = [], []
        for line in input_.split("\n"):
            splitted = line.split("   ")
            l.append(int(splitted[0]))
            r.append(int(splitted[-1]))
        return sorted(l), sorted(r)

    def a(self, input: Tuple[List[int], List[int]]) -> int:
        return sum(abs(x - y) for x, y in zip(*input))

    def b(self, input: Tuple[List[int], List[int]]) -> int:
        lookup = defaultdict(lambda: 0)
        l, r = input
        for n in r:
            lookup[n] += 1
        return sum(n * lookup[n] for n in l)


puzzle = Puzzle1()
puzzle.solve()
