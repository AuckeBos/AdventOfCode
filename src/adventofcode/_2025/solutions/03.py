from adventofcode._templates.v20231204.puzzle_to_solve import PuzzleToSolve


class Puzzle3(PuzzleToSolve):
    @property
    def day(self) -> int:
        return 3

    @property
    def year(self) -> int:
        return 2025

    @property
    def test_input(self) -> str:
        return """987654321111111
811111111111119
234234234234278
818181911112111"""

    @property
    def test_answer_a(self):
        return 357

    @property
    def test_answer_b(self):
        return 3121910778619

    def parse_input(self, input_: str) -> list[list[int]]:
        return [[int(char) for char in line] for line in input_.split("\n")]

    def max_battery(
        self, batteries: list[int], *, n_required_after: int
    ) -> tuple[int, int]:
        """Get the max battery where the remaining batteries have at least n_required_after batteries."""
        if len(batteries) <= n_required_after:
            raise ValueError("Not enough batteries found")
        for value in range(9, 0, -1):
            try:
                i = batteries.index(value)  # First battery of this value
            except ValueError:
                continue
            if (
                len(batteries) - i - 1 >= n_required_after
            ):  # Only use it if enough batteries remain
                return value, i
        raise ValueError("Broke the laws of physics")

    def max_joltage(self, batteries: list[int], n_batteries: int) -> int:
        """Find the max joltage of a list of batteries.

        Given that joltage is defined by n_batteries highest batteries concatenated.
        """
        selected_batteries: list[int] = []
        for k in range(n_batteries):
            battery, i = self.max_battery(
                batteries, n_required_after=n_batteries - k - 1
            )
            batteries = batteries[i + 1 :]  # Continue with all subsequent batteries
            selected_batteries.append(battery)
        return int("".join(str(b) for b in selected_batteries))

    def a(self, input_: list[list[int]]):
        return sum(self.max_joltage(row, 2) for row in input_)

    def b(self, input_: list[list[int]]):
        return sum(self.max_joltage(row, 12) for row in input_)


puzzle = Puzzle3()
puzzle.solve()
