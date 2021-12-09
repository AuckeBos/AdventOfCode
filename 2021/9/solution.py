import numpy as np

from helpers import read_input
from matrix import Matrix

# PT1: Get sum of risk level of low points
# PT2: Get sum of the len of the largest 3 basins

PART = 2


input = read_input("input", as_int=False)
raw_matrix = []
for row in input:
    raw_matrix.append([int(v) for v in row])
raw_matrix = np.array(raw_matrix)
matrix = Matrix(raw_matrix)
if PART == 1:
    print(sum([p.risk_level for p in matrix.low_points()]))
if PART == 2:
    print(matrix.get_basin_len_sum())