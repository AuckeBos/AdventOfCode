import math

from adventofcode._templates.v20231201.puzzle_to_solve import PuzzleToSolve
from adventofcode.helpers.base_matrix_v1 import BaseMatrixV1


class Matrix(BaseMatrixV1):
    def __init__(self, input_: str):
        self.parse_input(input_, ".")

    def find_part_numbers(self):
        return [
            self.get_full_part_number(i, j)
            for i, j in self.iter_topleft_to_bottomright()
            if self.is_start_of_part_number(i, j)
        ]

    def find_gear_ratios(self):
        return [
            self.get_gear_ratio(i, j)
            for i, j in self.iter_topleft_to_bottomright()
            if self.is_gear(i, j)
        ]

    def is_adjacent_to_symbol(self, i: int, j: int) -> bool:
        """
        Check if a given index is adjacent to a symbol (not a digit or ".")
        """
        return any(
            [
                (not self.data[x, y].isdigit()) and (not self.data[x, y] == ".")
                for x, y in self.adjacent_fields(i, j)
            ]
        )

    def get_adjacent_part_numbers(self, i: int, j: int) -> list[int]:
        """
        Get the adjacent part numbers of a given index.
        Use list({}) to remove duplicates. This assumes that we never have 2 equal part numbers adjacent to i,j. This turns out to be true.
        """
        return list(
            {
                self.get_full_part_number(x, y)
                for x, y in self.adjacent_fields(i, j)
                if self.is_part_of_part_number(x, y)
            }
        )

    def is_gear(self, i: int, j: int) -> bool:
        """
        A gear is a "*" with exactly 2 adjacent part numbers
        """
        return self.data[i, j] == "*" and len(self.get_adjacent_part_numbers(i, j)) == 2

    def get_gear_ratio(self, i: int, j: int) -> int:
        """
        The gear ratio is the product of the adjacent part numbers, if the i,j is a gear. Else 0.
        """
        return (
            math.prod(self.get_adjacent_part_numbers(i, j)) if self.is_gear(i, j) else 0
        )

    def get_full_part_number(self, i: int, j: int) -> int:
        """
        Get the full part number, given index i,j is the start of the part number
        """
        if not self.data[i, j].isdigit():
            raise ValueError(
                f"Index {i}, {j} is not a digit, hence cannot be part of a part number"
            )
        j_iter = j
        part_number = self.data[i, j]
        # Seek left
        while self.data[i, j_iter - 1].isdigit():
            part_number = self.data[i, j_iter - 1] + part_number
            j_iter -= 1
        # Seek right
        j_iter = j
        while self.data[i, j_iter + 1].isdigit():
            part_number += self.data[i, j_iter + 1]
            j_iter += 1
        return int(part_number)

    def is_part_of_part_number(self, i: int, j: int) -> bool:
        """
        Check if a given index is part of a part number. This is the case if
        - Self is a digit and
        - Self is adjacent to a symbol or Next is part of a part number
        """
        return (
            self.data[i, j].isdigit()  # Self is digit
            and (
                self.is_adjacent_to_symbol(i, j)  # Self is adjacent to a symbol
                or self.is_part_of_part_number(
                    i, j + 1
                )  # Next is part of the part number
            )
        )

    def is_start_of_part_number(self, i: int, j: int) -> bool:
        """
        i,j is the start of a part number if we have no digit on the left, and i,j is part of a part number
        """
        return (
            not self.data[
                i, j - 1
            ].isdigit()  # Left is not a digit (this would mean i,j is not the start)
            and self.is_part_of_part_number(i, j)  # i,j is part of a part number
        )


class Puzzle3(PuzzleToSolve):
    @property
    def day(self) -> int:
        return 3

    @property
    def year(self) -> int:
        return 2023

    @property
    def test_input(self) -> str:
        return """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""

    @property
    def test_answer_a(self):
        return 4361

    @property
    def test_answer_b(self):
        return 467835

    def a(self, input_: str):
        """
        Return the sum of all part numbers
        """
        matrix = Matrix(input_)
        numbers = matrix.find_part_numbers()
        result = sum(numbers)
        return result

    def b(self, input_: str):
        """
        Return the sum of all gear ratios
        """
        matrix = Matrix(input_)
        gear_ratios = matrix.find_gear_ratios()
        result = sum(gear_ratios)
        return result


puzzle = Puzzle3()
puzzle.solve()
