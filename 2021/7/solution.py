import numpy as np
import sys
from helpers import read_input

# PT1: Cost 1 per step
# PT2: Cum cost per step
PART = 2
USE_CUM_COST = PART == 2

positions = read_input("input", split_on=",")
positions = np.array(positions)
max_pos = np.max(positions)
# Costs will contain at index r,c the costs of moving crab r to posistion c
costs = np.full((len(positions), max_pos), max_pos)
# taking n steps costs n fuel
cost_for_n_steps = list(range(max_pos + 1))
if not USE_CUM_COST:
    cum_cost_for_n_steps = cost_for_n_steps
else: # Else cost for n steps is the cum sum of n steps
    cum_cost_for_n_steps = [sum(cost_for_n_steps[:i + 1]) for i in range(max_pos + 1)]
cum_cost_for_n_steps = np.array(cum_cost_for_n_steps)
# For each col, the num of steps to go to that col is the current pos minus the
# index of that col. Save the cost for moving that amount of steps in the col position
for i in range(costs.shape[1]):
    costs[:, i] = cum_cost_for_n_steps[np.abs(positions - i)]
# Search the col with the lowest cost sum
colsums = np.sum(costs, axis=0)
cheapest = np.argmin(colsums)
cost = np.sum(costs[:, cheapest])
print(cost)
