from itertools import product
from typing import List

import numpy as np
from numpy.typing import NDArray

from digit import Digit


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
        - Convert the matrix into a list of mapping. This is a list of all possible
        combinations, where we take one col as true value out of all true values of
        the row
        - Check each mapping. As soon as we find a valid one, return it
        """
        matrix = self.get_option_matrix()
        mappings = list(product(*[np.where(matrix[char])[0] for char in range(7)]))
        for mapping in mappings:
            if self.check_mapping(mapping):
                return mapping
        raise ValueError("Mapping cannot be found")

    # Mapping is correct if all digits occur after the mapping
    def check_mapping(self, mapping: List[int]):
        digits = [digit.get_val_by_mapping(mapping) for digit in self.inputs]
        return len(set(range(0, 10)).intersection(digits)) == 10

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