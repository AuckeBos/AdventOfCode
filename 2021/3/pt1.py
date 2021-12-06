import numpy as np

from helpers import read_input, bit_list_to_int

rows = read_input(as_int=False)
matrix = np.array([list(r) for r in rows]).astype(float)
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

gamma = bit_list_to_int(gamma)
epsilon = bit_list_to_int(epsilon)

result = gamma * epsilon
print(result)

