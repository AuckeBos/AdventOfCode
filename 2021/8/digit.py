from typing import List

import numpy as np
from numpy.typing import NDArray

alphabet = "abcdefghijklmnopqrstuvwxyz"


class Digit:

    # Map the length of the input to the pos that are present in the original mapping
    INPUT_LEN_TO_PRESENT_POS = {
        2: [2, 5],
        4: [1, 2, 3, 5],
        3: [0, 2, 5],
        7: [0, 1, 2, 3, 4, 5, 6],
    }

    CHARS_TO_DIGIT = {
        "abcefg": 0,
        "cf": 1,
        "acdeg": 2,
        "acdfg": 3,
        "bcdf": 4,
        "abdfg": 5,
        "abdefg": 6,
        "acf": 7,
        "abcdefg": 8,
        "abcdfg": 9,
    }

    input: str

    def __init__(self, inp: str):
        self.input = "".join(sorted(inp))

    # Simple digits are those that we can extract the val from by looking at the n_chars
    def is_simple_digit(self):
        return len(self.input) in [2, 3, 4, 7]

    def get_option_matrix(self) -> NDArray:
        """
        Find all possible mappings of letters to positions. These are saved in a np
        array of shape (7,7):
        rows: letters a - f
        columns: positions 1 - 7 (eg top, top left, top right, middle, bottom left,
            bottom right, bottom)
        values: booleans, a 1 in r,c means that letter r might correspond to position c.
        Initially all values are 1. Stop until each row has one 1

        For a digit, we can exclude som possibilities, depending on the number of chars
        :return Boolean NDArray of shape (7,7). False is set on own chars on all
        absent positions
        """
        # All options open
        mapping = np.full((7, 7), dtype=bool, fill_value=1)
        if self.is_simple_digit():
            present_chars = [alphabet.index(c) for c in self.input]
            absent_chars = list(set(range(7)).difference(present_chars))
            present_positions = self.INPUT_LEN_TO_PRESENT_POS[len(self.input)]
            absent_positions = list(set(range(7)).difference(present_positions))

            # The current chars do not map to absent positions
            if absent_positions:
                for char in present_chars:
                    mapping[char, absent_positions] = False
            # Absent chars do not map to present positions
            if present_positions:
                for char in absent_chars:
                    mapping[char, present_positions] = False

        return mapping

    def get_val_by_mapping(self, mapping: List[int]):
        """
        Convert self.present_chars to a digit via a mapping
        :param mapping: The mapping, maps char index to new char index
        :return: int the digit value
        """
        mapping = np.array(mapping)
        new_indices = sorted(mapping[[alphabet.index(c) for c in self.input]])
        new_chars = "".join([alphabet[i] for i in new_indices])
        return self.CHARS_TO_DIGIT.get(new_chars, 0)
