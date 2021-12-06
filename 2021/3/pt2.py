import numpy as np

from helpers import read_input, bit_list_to_int


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
        # get most common or least common bit, by checking if frac 1 > or < half n rows
        bit = int(sum(col) / n_rows >= 0.5 if keep_max else sum(col) / n_rows < 0.5)
        # Keep only rows that match bit
        indices = col == bit
        cur_matrix = cur_matrix[indices]
        # If done, return
        if len(cur_matrix) == 1:
            return cur_matrix[0].tolist()

rows = read_input(as_int=False)
matrix = np.array([list(r) for r in rows]).astype(float)
oxygen = get_row(matrix, True)
co2 = get_row(matrix, False)

oxygen = bit_list_to_int(oxygen)
co2 = bit_list_to_int(co2)


result = oxygen * co2
print(result)

