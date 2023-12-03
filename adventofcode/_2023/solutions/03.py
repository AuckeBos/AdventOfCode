import math
from adventofcode._templates.puzzle_to_solve import PuzzleToSolve
import numpy as np


class Matrix:
    data: np.ndarray
    
    def __init__(self, input_: str):
        # Create numpy character matrix from input
        self.matrix = np.array([list(line) for line in input_.split("\n")])
        # Surround matrix with ".", to make sure we don't get index errors
        self.matrix = np.pad(self.matrix, 1, constant_values=".")
    
    def find_part_numbers(self):
        return [
            self.get_full_part_number(i, j)
            for i in range(1, self.matrix.shape[0] - 1)
            for j in range(1, self.matrix.shape[1] - 1)
            if self.is_start_of_part_number(i, j)
        ]

    def find_gear_ratios(self):
        return [
            self.get_gear_ratio(i, j)
            for i in range(1, self.matrix.shape[0] - 1)
            for j in range(1, self.matrix.shape[1] - 1)
            if self.is_gear(i, j)
        ]

        
    
    def adjacent_fields(self, i: int, j: int):
        """
        Get the adjacent fields of a given index
        """
        return [
            (i - 1, j - 1), (i - 1, j), (i - 1, j + 1),
            (i, j - 1), (i, j + 1),
            (i + 1, j - 1), (i + 1, j), (i + 1, j + 1)
        ]
    
    
    def is_adjacent_to_symbol(self, i: int, j: int) -> bool:
        """
         Check if a given index is adjacent to a symbol (not a digit or ".")
         """
        return any(
            [
                (not self.matrix[x, y].isdigit()) and (not self.matrix[x, y] == ".") for x, y in self.adjacent_fields(i, j)
            ]
        )
    
    def get_adjacent_part_numbers(self, i: int, j: int) -> list[int]:
        """
        Get the adjacent part numbers of a given index.
        Use list({}) to remove duplicates. This assumes that we never have 2 equal part numbers adjacent to i,j. This turns out to be true.
        """
        return list({
            self.get_full_part_number(x, y) for x, y in self.adjacent_fields(i, j) if self.is_part_of_part_number(x, y)
        })
    
    def is_gear(self, i: int, j: int) -> bool:
        """
        A gear is a "*" with exactly 2 adjacent part numbers
        """
        return (
            self.matrix[i, j] == "*" and
            len(self.get_adjacent_part_numbers(i, j))  == 2
        )
    
    def get_gear_ratio(self, i: int, j: int) -> int:
        """
        The gear ratio is the product of the adjacent part numbers, if the i,j is a gear. Else 0.
        """
        return math.prod(self.get_adjacent_part_numbers(i, j)) if self.is_gear(i, j) else 0
    
    def get_full_part_number(self, i: int, j: int) -> int:
        """
        Get the full part number, given index i,j is the start of the part number
        """
        if not self.matrix[i, j].isdigit():
            raise ValueError(f"Index {i}, {j} is not a digit, hence cannot be part of a part number")
        j_iter = j
        part_number = self.matrix[i, j]
        # Seek left
        while self.matrix[i, j_iter - 1].isdigit():
            part_number = self.matrix[i, j_iter - 1] + part_number
            j_iter -= 1
        # Seek right
        j_iter = j
        while self.matrix[i, j_iter + 1].isdigit():
            part_number += self.matrix[i, j_iter + 1]
            j_iter += 1
        return int(part_number)

    def is_part_of_part_number(self, i: int, j: int) -> bool:
        """
        Check if a given index is part of a part number. This is the case if
        - Self is a digit and 
        - Self is adjacent to a symbol or Next is part of a part number
        """
        return (
            self.matrix[i, j].isdigit() # Self is digit
            and
            (
                self.is_adjacent_to_symbol(i, j) # Self is adjacent to a symbol
                or
                self.is_part_of_part_number(i, j + 1) # Next is part of the part number
            )
        )        
    
    def is_start_of_part_number(self, i: int, j: int) -> bool:
        """
        i,j is the start of a part number if we have no digit on the left, and i,j is part of a part number
        """
        return (
            not self.matrix[i, j - 1].isdigit() # Left is not a digit (this would mean i,j is not the start)
            and self.is_part_of_part_number(i, j) # i,j is part of a part number
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
