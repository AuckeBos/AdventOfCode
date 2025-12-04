import numpy as np

from adventofcode._templates.v20231204.puzzle_to_solve import PuzzleToSolve
from adventofcode.helpers.base_matrix import BaseMatrix, Position


class Puzzle4(PuzzleToSolve):
    @property
    def day(self) -> int:
        return 4

    @property
    def year(self) -> int:
        return 2025

    @property
    def test_input(self) -> str:
        return """..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@."""

    @property
    def test_answer_a(self) -> int:
        return 13

    @property
    def test_answer_b(self) -> int:
        return 43

    def parse_input(self, input_: str) -> BaseMatrix:
        return BaseMatrix(input_, dtype=str, pad=None)

    def is_removable_roll(self, matrix: BaseMatrix, position) -> bool:
        """A position is a removable roll if:

        - It is a roll ("@")
        - It has 3 or fewer adjacent rolls (including diagonals)
        """
        return (
            matrix[position] == "@"
            and np.sum(
                np.array(
                    matrix.adjacent_values(
                        position, include_axis=True, include_diagonal=True
                    )
                )
                == "@"
            )
            <= 3
        )

    def removable_rolls(self, matrix: BaseMatrix) -> list[Position]:
        """Find all removable rolls in the matrix."""
        return [
            position
            for position in matrix.iter_topleft_to_bottomright()
            if self.is_removable_roll(matrix, position)
        ]

    def a(self, input_: BaseMatrix) -> int:
        """Count the number of removable rolls in the matrix."""
        return len(self.removable_rolls(input_))

    def remove_rolls(self, matrix: BaseMatrix, positions: list[Position]) -> BaseMatrix:
        """Remove a list of rolls from the matrix."""
        for position in positions:
            matrix[position] = "."
        return matrix

    def b(self, input_: BaseMatrix) -> int:
        """Remove rolls until no more removable rolls exist. Return the number of rolls removed."""
        rolls_removed = 0
        while rolls_to_remove := len(self.removable_rolls(input_)):
            input_ = self.remove_rolls(input_, self.removable_rolls(input_))
            rolls_removed += rolls_to_remove
        return rolls_removed


puzzle = Puzzle4()
puzzle.solve()
