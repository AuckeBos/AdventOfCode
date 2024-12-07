from adventofcode._templates.v20231204.puzzle_to_solve import PuzzleToSolve


def add(a, b):
    return a + b


def multiply(a, b):
    return a * b


def concatenate(a, b):
    return int(str(a) + str(b))


class Puzzle7(PuzzleToSolve):
    @property
    def day(self) -> int:
        return 7

    @property
    def year(self) -> int:
        return 2024

    @property
    def test_input(self) -> str:
        return """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"""

    @property
    def test_answer_a(self):
        return 3749

    @property
    def test_answer_b(self):
        return 11387

    def parse_input(self, input_: str) -> list[tuple[int, list[int]]]:
        lines = input_.split("\n")
        return [
            (int(line.split(":")[0]), list(map(int, line.split(":")[1].split())))
            for line in lines
        ]

    def can_be_true(
        self, answer: int, values: list[int], operators: list[callable] = None
    ):
        if len(values) == 1:
            return values[0] == answer
        for operator in operators:
            if self.can_be_true(
                answer,
                [operator(values[0], values[1]), *values[2:]],
                operators,
            ):
                return True
        return False

    def a(self, input_: list[tuple[int, list[int]]]) -> int:
        return sum(
            [
                answer
                for answer, values in input_
                if self.can_be_true(answer, values, [add, multiply])
            ]
        )

    def b(self, input_: list[tuple[int, list[int]]]) -> int:
        return sum(
            [
                answer
                for answer, values in input_
                if self.can_be_true(answer, values, [add, multiply, concatenate])
            ]
        )


puzzle = Puzzle7()
puzzle.solve()
