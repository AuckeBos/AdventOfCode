import numpy as np

from adventofcode._templates.v20231204.puzzle_to_solve import PuzzleToSolve
from adventofcode.helpers.parsing import as_matrix


class Puzzle2(PuzzleToSolve):
    MIN_DISTANCE = 1
    MAX_DISTANCE = 3

    @property
    def day(self) -> int:
        return 2

    @property
    def year(self) -> int:
        return 2024

    @property
    def test_input(self) -> str:
        return """7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9"""

    @property
    def test_answer_a(self):
        return 2

    @property
    def test_answer_b(self):
        return 4

    def parse_input(self, input_: str) -> np.matrix:
        return as_matrix(input_, padding=-1)

    def compute_validity(self, matrix: np.matrix) -> list[int]:
        """
        Copy the matrix, overlay shifted by one, and compute the requirements for a valid row.
        Return the indices of the valid rows (the rows where all cells are valid)
        """
        mask = matrix.copy()
        directions_col = np.where(matrix[:, 0] < matrix[:, 1], 1, -1)
        mask = matrix[:, :-1]
        matrix = matrix[:, 1:]
        directions = np.repeat(directions_col, matrix.shape[1]).reshape(matrix.shape)
        valid_cells = np.where(
            (matrix == -1)
            | (
                (np.abs(matrix - mask) >= self.MIN_DISTANCE)
                & (np.abs(matrix - mask) <= self.MAX_DISTANCE)
                & (np.multiply(matrix - mask, directions) > 0)
            ),
            1,
            0,
        )
        return list(np.argwhere(np.all(valid_cells, axis=1)).flatten())

    def a(self, matrix: np.matrix) -> int:
        """
        Count the valid rows.
        """
        return len(self.compute_validity(matrix))

    def b(self, matrix: np.matrix) -> int:
        """
        Create all matrix configurations: the original matrix and all matrices with one column removed.
        For each matrix, find the valid rows. Return the count of the unique valid rows.
        """
        matrices = [
            matrix,
            *map(
                lambda col: np.delete(matrix.copy(), col, axis=1),
                range(matrix.shape[1]),
            ),
        ]
        return len(
            {row for matrix in matrices for row in self.compute_validity(matrix)}
        )


puzzle = Puzzle2()
puzzle.solve()
