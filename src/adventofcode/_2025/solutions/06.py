from math import prod

import numpy as np

from adventofcode._templates.v20231204.puzzle_to_solve import PuzzleToSolve
from adventofcode.helpers.base_matrix import BaseMatrix


class Puzzle6(PuzzleToSolve):
    """Puzzle for 2025 Day 6.

    Attributes:
        _PAD: The character used to pad missing digits in numbers
    """

    _PAD = "X"

    @property
    def day(self) -> int:
        return 6

    @property
    def year(self) -> int:
        return 2025

    @property
    def test_input(self) -> str:
        return """123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  """

    @property
    def test_answer_a(self) -> int:
        return 4277556

    @property
    def test_answer_b(self) -> int:
        return 3263827

    def _pad_columns(self, input_: str) -> str:
        """Pad the columns in the input so that all numbers have the same number of digits.

        - Check each cell. If its a digit, continue
        - Else, check if all cells in the column are space. If so, we are at a column
            delimiter, so leave " "
        - Else, at least one number is a digit, hence this cell should be padded
        """
        matrix = BaseMatrix(
            input_,
            None,
        )
        for position in matrix.iter_topleft_to_bottomright():
            if matrix[position] != " " or np.all(matrix.data[:, position.j] == " "):
                continue
            matrix[position] = self._PAD
        return str(matrix)

    def parse_input(self, input_: str) -> BaseMatrix:
        """Parse the input into a BaseMatrix with multi-character cells."""
        return BaseMatrix(
            self._pad_columns(input_),
            None,
            split_columns_on=" ",
        )

    def a(self, matrix: BaseMatrix) -> int:
        return sum(  # Sum all column results
            (  # The function to apply to this column, based on the last item of this column
                sum if column[-1][0] == "+" else prod
            )(
                [  # Get all numbers in this column, excluding last row and removing X's
                    int(x.strip(self._PAD)) for x in column[:-1]
                ]
            )
            for column in [  # For each column
                col.tolist()[0] for col in matrix.columns
            ]
        )

    def b(self, matrix: BaseMatrix) -> int:
        return sum(  # Sum all column results
            (  # The function to apply to each charcol for this column, based on the last item of this column
                sum if column[-1][0] == "+" else prod
            )(
                [  # Apply the correct operator to each charcol
                    int(  # Cast concats to int
                        "".join(  # Concat all non-pad strings
                            row[c_index]
                            for row in column[
                                :-1
                            ]  # Each row in this column, excluding the last operator row
                            if row[c_index]
                            != self._PAD  # Each char in this charcol from right to left, if not pad
                        )
                    )
                    for c_index in range(
                        len(column[0]) - 1,  # The charsize of EACH cell in this column
                        -1,
                        -1,  # From right to left
                    )
                ]
            )
            for column in [  # For each column
                col.tolist()[0] for col in matrix.columns
            ]
        )


puzzle = Puzzle6()
puzzle.solve()
