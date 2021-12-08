from typing import Optional, List
import string

import numpy as np
from numpy.typing import NDArray

alphabet = "abcdefghijklmnopqrstuvwxyz"


class Digit:
    # Map a 0-9 int to its len in chars
    VAL_TO_INPUT_LEN = {0: 6, 1: 2, 2: 5, 3: 5, 4: 4, 5: 5, 6: 6, 7: 3, 8: 7, 9: 6}

    # Map a digit with len chars to the pos that are present in the original mapping
    INPUT_LEN_TO_PRESENT_POS = {
        2: [2, 5],
        3: [0, 2, 5],
        4: [1, 2, 3, 5],
        5: [0, 3, 6],
        6: [0, 1, 5, 6],
        7: [0, 1, 2, 3, 4, 5, 6],
    }

    # Map a digit with len chars to the pos that are absent in the original mapping
    INPUT_LEN_TO_ABSENT_POS = {
        2: [0, 1, 3, 4, 6],
        3: [1, 3, 4, 6],
        4: [0, 4, 6],
        5: [],
        6: [],
        7: [],
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

    # Chars 0-6 exist, these are a-g
    ALL_POSITIONS = set(range(0, 7))

    # Char indices: a = 0, b = 1

    # Index exists in this list if the char belonging to it was present in the input
    present_chars: List[int]
    # All char indices except those in present_positions
    absent_chars: List[int]

    # Index exists in this list if the position should be 'on' for self.val. Eg for a
    # digit with val 1, present_positions_for_val = [2,5] (namely c, f)
    present_positions: List[int]
    # All char indices except those in present_positions_for_val
    absent_positions: List[int]

    def __init__(self, inp: str):
        inp = sorted(inp)
        self.present_chars = [alphabet.index(c) for c in inp]
        self.absent_chars = list(Digit.ALL_POSITIONS.difference(self.present_chars))
        self.present_positions = self.INPUT_LEN_TO_PRESENT_POS[len(inp)]
        self.absent_positions = self.INPUT_LEN_TO_ABSENT_POS[len(inp)]

    # Simple digits are those that we can extract the val from by looking at the n_chars
    def is_simple_digit(self):
        return len(self.present_chars) in [2, 3, 4, 7]

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
        # The current chars do not map to absent positions
        if self.absent_positions:
            for char in self.present_chars:
                mapping[char, self.absent_positions] = False
        # Absent chars do not map to present positions
        if self.present_positions:
            for char in self.absent_chars:
                mapping[char, self.present_positions] = False

        return mapping

    def get_val_by_mapping(self, mapping: List[int]):
        """
        Convert self.present_chars to a digit via a mapping
        :param mapping: The mapping, maps char index to new char index
        :return: int the digit value
        """
        mapping = np.array(mapping)
        new_indices = mapping[self.present_chars]
        new_chars = "".join(sorted([alphabet[i] for i in new_indices]))
        value = 0
        if new_chars in self.CHARS_TO_DIGIT:
            value = self.CHARS_TO_DIGIT[new_chars]
        return value
