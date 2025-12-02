import sys
from functools import cache
from typing import Callable

from adventofcode._templates.v20231204.puzzle_to_solve import PuzzleToSolve

sys.setrecursionlimit(10000000)


class Puzzle2(PuzzleToSolve):
    @property
    def day(self) -> int:
        return 2

    @property
    def year(self) -> int:
        return 2025

    @property
    def test_input(self) -> str:
        return """11-22,95-115,998-1012,1188511880-1188511890,222220-222224,
1698522-1698528,446443-446449,38593856-38593862,565653-565659,
824824821-824824827,2121212118-2121212124"""

    @property
    def test_answer_a(self):
        return 1227775554

    @property
    def test_answer_b(self):
        return 4174379265

    def parse_input(self, input_: str) -> list[tuple[int, int]]:
        return [
            (int(start), int(end))
            for start, end in (line.split("-") for line in input_.split(","))
        ]

    @staticmethod
    def is_repeating_number(number: int) -> bool:
        """Check if the number repeats itself exactly once."""
        number_str = str(number)
        length = len(number_str)
        if length % 2 != 0:
            return False
        half = length // 2
        return number_str[:half] == number_str[half:]

    @cache
    def sum_failures(
        self, start: int, end: int, failure_func: Callable[[int], int]
    ) -> int:
        """Sum all failing numbers, using the provided failure function."""
        result = 0
        while start <= end:
            if failure_func(start):
                result += start
            start += 1

        return result

    def a(self, input_: list[tuple[int, int]]):
        return sum(
            self.sum_failures(start, end, self.is_repeating_number)
            for start, end in input_
        )

    @cache
    def is_number_with_repeating_pattern(self, number: int) -> bool:
        """Check if the number consists of one pattern repeating twice or more."""
        number_str = str(number)
        n = 1
        while n <= len(number_str) // 2:
            pattern = number_str[:n]
            if len(number_str) % n == 0 and number_str.count(pattern) * n == len(
                number_str
            ):
                return True
            n += 1
        return False

    def b(self, input_: list[tuple[int, int]]):
        return sum(
            self.sum_failures(start, end, self.is_number_with_repeating_pattern)
            for start, end in input_
        )


puzzle = Puzzle2()
puzzle.solve()
