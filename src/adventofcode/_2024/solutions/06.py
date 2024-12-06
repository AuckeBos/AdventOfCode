from adventofcode._templates.v20231204.puzzle_to_solve import PuzzleToSolve


class Puzzle6(PuzzleToSolve):
    @property
    def day(self) -> int:
        return 6

    @property
    def year(self) -> int:
        return 2024

    @property
    def test_input(self) -> str:
        return """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""

    @property
    def test_answer_a(self):
        return 41

    @property
    def test_answer_b(self):
        return None

    def parse_input(self, input_: str):
        return None

    def a(self, input_: str):
        return -1

    def b(self, input_: str):
        return -1


puzzle = Puzzle6()
puzzle.solve()
