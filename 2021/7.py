import numpy as np

from aocd.models import Puzzle

puzzle = Puzzle(year=2021, day=7)
positions = np.array([int(x) for x in puzzle.input_data.split(",")])
max_pos = np.max(positions)

# costs_matrix will contain at index r,c the costs of moving crab r to position c
costs_matrix_a = np.full((len(positions), max_pos), max_pos)
costs_matrix_b = np.full((len(positions), max_pos), max_pos)

# costs maps nr of steps to the costs to make that nr of steps
costs_pt_a = np.array(list(range(max_pos + 1)))
# Cost for n steps is the cum sum of n steps
costs_pt_b = np.array([sum(costs_pt_a[:i]) for i in range(1, max_pos + 2)])

# For each col, save the costs of going to that col
for i in range(costs_matrix_a.shape[1]):
    costs_matrix_a[:, i] = costs_pt_a[np.abs(positions - i)]
    costs_matrix_b[:, i] = costs_pt_b[np.abs(positions - i)]

# Search the col with the lowest cost sum
cheapest_col_pt_a = np.argmin(np.sum(costs_matrix_a, axis=0))
cheapest_col_pt_b = np.argmin(np.sum(costs_matrix_b, axis=0))
# Sum the costs of moving all crabs to the cheapest col
puzzle.answer_a = np.sum(costs_matrix_a[:, cheapest_col_pt_a])
puzzle.answer_b = np.sum(costs_matrix_b[:, cheapest_col_pt_b])
