from adventofcode._templates.v20231204.puzzle_to_solve import PuzzleToSolve


class Puzzle5(PuzzleToSolve):
    @property
    def day(self) -> int:
        return 5

    @property
    def year(self) -> int:
        return 2025

    @property
    def test_input(self) -> str:
        return """3-5
10-14
16-20
12-18

1
5
8
11
17
32"""

    @property
    def test_answer_a(self) -> int:
        return 3

    @property
    def test_answer_b(self) -> int:
        return 14

    def parse_input(self, input_: str) -> tuple[list[tuple[int, int]], list[int]]:
        return (
            [
                tuple(map(int, line.split("-")))
                for line in input_.split("\n\n")[0].splitlines()
            ],
            [int(line) for line in input_.split("\n\n")[1].splitlines()],
        )  # type: ignore

    def a(self, input_: tuple[list[tuple[int, int]], list[int]]):
        database, ingredients = input_
        return sum(
            1
            for number in ingredients
            if any(start <= number <= end for start, end in database)
        )

    def b(self, input_: tuple[list[tuple[int, int]], list[int]]):
        database = sorted(input_[0])
        merged: list[tuple[int, int]] = [database.pop(0)]
        for start, end in database:
            # if item is after last range, add new range
            if merged[-1][1] < start - 1:
                merged.append((start, end))
            # It overlaps. Add it to the last range
            else:
                merged[-1] = (merged[-1][0], max(merged[-1][1], end))
        result = sum(end - start + 1 for start, end in merged)
        return result


puzzle = Puzzle5()
puzzle.solve()
