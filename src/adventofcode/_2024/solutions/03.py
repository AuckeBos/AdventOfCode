import re

from adventofcode._templates.v20231204.puzzle_to_solve import PuzzleToSolve


class Puzzle3(PuzzleToSolve):
    @property
    def day(self) -> int:
        return 3

    @property
    def year(self) -> int:
        return 2024

    @property
    def test_input(self) -> str:
        return "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"

    @property
    def test_input_alternative(self) -> str:
        return (
            "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
        )

    @property
    def test_answer_a(self):
        return 161

    @property
    def test_answer_b(self):
        return 48

    def parse_input(self, input_: str):
        return input_

    def a(self, input_: str):
        """Find all muls, and sum the results"""
        pattern = r"mul\((\d+),(\d+)\)"
        matches = re.findall(pattern, input_)
        return sum(int(a) * int(b) for a, b in matches)

    def b(self, input_: str):
        """
        Find all muls, don'ts, and dos. Sum the results of the mults,
        but only if the do flag is set.
        """
        pattern = r"(?:(mul)\((\d+),(\d+)\))|(?:(don\'t)\(\))|(?:(do)\(\))"
        matches = re.findall(pattern, input_)
        do = True
        result = 0
        for match in matches:
            operation = match[0] or match[3] or match[4]
            if do and operation == "mul":
                result += int(match[1]) * int(match[2])
            do = do and operation != "don't" or operation == "do"
        return result


puzzle = Puzzle3()
puzzle.solve()
