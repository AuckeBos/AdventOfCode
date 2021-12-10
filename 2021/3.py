import numpy as np
from aocd.models import Puzzle
from bitstring import BitArray
from numpy.typing import NDArray

from helpers import bit_list_to_int


def pt_1(matrix: NDArray):
    n_rows = matrix.shape[0]
    # Sum cols
    sums = np.sum(matrix, axis=0)
    # Compute frac of rows that is 1
    frac_1 = sums / n_rows
    # Most common: 1 if frac one >=
    most_common = (frac_1 >= 0.5).astype(int)

    # Convert to list
    gamma = list(most_common)
    # Bit flip for epsilon
    epsilon = [(x + 1) % 2 for x in gamma]

    gamma = BitArray(gamma).uint
    epsilon = BitArray(epsilon).uint

    result = gamma * epsilon
    return result


def pt_2(matrix: NDArray):
    def get_row(matrix, keep_max):
        """
        Get the row for criterium
        :param frame:
        :param keep_max: If true, search oxygen, else search co2
        :return:
        """
        cur_matrix = matrix
        # loop over cols
        for i in range(matrix.shape[1]):
            n_rows = cur_matrix.shape[0]
            col = cur_matrix[:, i]
            # get most/least common bit, by checking if frac 1 > or < half n rows
            bit = int(sum(col) / n_rows >= 0.5 if keep_max else sum(col) / n_rows < 0.5)
            # Keep only rows that match bit
            indices = col == bit
            cur_matrix = cur_matrix[indices]
            # If done, return
            if len(cur_matrix) == 1:
                return cur_matrix[0].tolist()

    oxygen = get_row(matrix, True)
    co2 = get_row(matrix, False)

    oxygen = BitArray(oxygen).uint
    co2 = BitArray(co2).uint
    return oxygen * co2


puzzle = Puzzle(year=2021, day=3)
lines = puzzle.input_data.splitlines()
matrix = np.array([list(l) for l in lines]).astype(float)
puzzle.answer_a = pt_1(matrix)
puzzle.answer_b = pt_2(matrix)
