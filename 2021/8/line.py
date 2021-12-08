from typing import List

import numpy as np
from numpy.typing import NDArray

from digit import Digit
import string


class Line:
    inputs: List[Digit]
    outputs: List[Digit]
    matrix: NDArray

    def __init__(self, input: str):
        inputs, outputs = input.split(" | ")
        self.inputs = [Digit(input) for input in inputs.split(" ")]
        self.outputs = [Digit(output) for output in outputs.split(" ")]

    def get_option_matrix(self):
        """
        The option matrix is a (7,7) matrix with bools. The value is true if char r
        might map to index c. Start with all true. perform AND on all digit matrices
        :return:
        """
        matrix = np.full((7, 7), dtype=bool, fill_value=True)
        for digit in self.inputs:
            digit_matrix = digit.get_option_matrix()
            matrix = np.logical_and(matrix, digit_matrix)
        return matrix

    def find_mapping(self) -> List[int]:
        """
        Find the mapping of letters to positions:
        - Get the option matrix. This matrix might (probably will) contain more tha
        n1 true value per row
        - Convert the matrix to a list of matrices, one for each true value in the
        original matrix. The row for that true value will contain only false values
        in the rest of the cols
        - Convert each matrix to a mapping. The mapping maps the original char value
        (index) to the new char value (value)
        - Check each mapping. As soon as we find a valid one, return it
        """
        matrix = self.get_option_matrix()
        matrices = self.split_matrix(matrix)
        mappings = self.matrices_to_mappings(matrices)
        for mapping in mappings:
            if self.check_mapping(mapping):
                return mapping
        raise ValueError("Mapping cannot be found")

    # Mapping is correct if all digits occur after the mapping
    def check_mapping(self, mapping: List[int]):
        digits = [digit.get_val_by_mapping(mapping) for digit in self.inputs]
        return len(set(range(0, 10)).intersection(digits)) == 10

    def matrices_to_mappings(self, matrices: List[NDArray]):
        # Each matrix to a mapping. Mapping maps char id to new char id
        mappings = [
            [np.where(matr[char])[0][0] for char in range(matr.shape[0])]
            for matr in matrices
        ]

        return mappings

    def compute_output(self) -> int:
        """
        The output converts each Digit to a new value, return the concatenated value
        as int
        :return: int
        """
        mapping = self.find_mapping()
        result = int(
            "".join([str(digit.get_val_by_mapping(mapping)) for digit in self.outputs])
        )
        return result

    @classmethod
    def split_matrix(cls, matrix: NDArray) -> List[NDArray]:
        """
        Matrix with possible more than 1 true value per row to:
        List of matrices with 1 true value per row
        :param matrix: (7,7) boolean matrix. True if r could map to c
        :return:  List o (7,7) matrices.
        """
        # Duplicate matrix, where each row with more than 1 True is copied to new
        # matrices with 1 true per matrix
        matrices = []
        for char in range(matrix.shape[0]):
            options = np.where(matrix[char])[0]
            if len(options) == 1:
                continue
            for option in options:
                copy = np.copy(matrix)
                copy[char] = False
                copy[char, option] = True
                matrices.extend(cls.split_matrix(copy))
        if not matrices:
            matrices.append(matrix)
        return matrices
