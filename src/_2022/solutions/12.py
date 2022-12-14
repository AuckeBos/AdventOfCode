import math
import re
import string
import sys
from copy import deepcopy
from typing import Tuple

import numpy as np
from numpy.typing import NDArray

from src._2022.puzzle_to_solve import PuzzleToSolve
import string


class Map:
    """
    The map contains the matrix of heights, and implements Dijkstras
    Attributes
    ----------
    matrix: NDArray
        Matrix of heights, as ints. The values are the index in S{alphabet}E. Hence the start height is 0,
        end height is 27, and all others height is the index in the alphabet
    goal: int
        The goal height (27)
     distances_to_start: NDArray
        Set during Dijkstras. Contains in each cell the least amount of steps needed to go from the start cell to here
    visited_nodes: NDArray
        Boolean array. All false at start. During Dijkstra, set to true whenever a cell is visited (such that we
        wont re-visit)
    climbing: bool
        Set to True for b). In b), we want to compute all distances to the end (such that we can then find the 'a' cell
        with the smallest distance to end). When true, we change the algorithm as follows:
        - The height of the start node (which is actually the end node) is set to 27 (max height)
        - The start position is the node with height max, instead of height 0
        - During Sijkstras, we disallow movements to more than 1 lower, instead of to more than 1 higher
    DIRECTIONS: List[Tuple[int, int]]
        List of possible directions to go to from a cell (delta)
    max_val: int
        Used as max int. Dont use sys.maxsize to prevent memory errors.


    """
    matrix: NDArray  # r,c
    letter_to_height = 'S' + string.ascii_lowercase + 'E'
    goal = letter_to_height.index('E')
    distances_to_start: NDArray
    visited_nodes: NDArray
    climbing: bool

    DIRECTIONS = [
        (0, -1),
        (-1, 0),
        (0, 1),
        (1, 0),
    ]
    max_val = 99999999

    def __init__(self, input_: str, climbing=True):
        self.climbing = climbing
        self.parse_input(input_)

    def parse_input(self, input_: str):
        """
        Parse the input. Replace all letters with the height of the letter. Split items by ' ' and replace newlines with
        ';'. Now np.matrix() reads correctly, then convert to ndarray. If self.climbing, set the height of the start
        node to self.goal: In this case we start at the end, hence the start isn't at height 0 but at hight max. Set
        distances to start to max, except for start. Set visited nodes to all false
        """
        int_input = ' '.join(
            [str(self.letter_to_height.index(x)) if x in self.letter_to_height else x for x in input_]).replace(" \n",
                                                                                                              ";")
        self.matrix = np.array(np.matrix(int_input))
        if not self.climbing:
            self.matrix[tuple(np.argwhere(self.matrix == 0)[0])] = self.goal
        self.distances_to_start = np.full(self.matrix.shape, self.max_val, dtype=int)
        self.distances_to_start[self.start_pos] = 0
        self.visited_nodes = np.full(self.matrix.shape, 0, dtype=bool)

    def compute_min_distances_to_start_for_neighbors_of(self, pos: Tuple[int, int]):
        """
        Given that the min_distance_to_start for pos is set, compute the distances_to_start for all its neighbors
        - For all directions (top left bottom right):
            - If going this direction is outside of the matrix, skip it
            - If this direction is more than 1 up (climbing) or down (not climbing), skip it: Cannot go here
            - Else set the distances_to_start of the new cell to the minimum of the current distances_to_start of that cell,
                and the current distance + 1
        - Set self to visited
        - Return True if all nodes are visited
        """
        current_distance = self.distances_to_start[pos]
        for direction in self.DIRECTIONS:
            new_pos = tuple(np.array(pos) + direction)

            # If cannot index, out of board. skip
            if self.matrix.shape[0] - 1 < new_pos[0] or new_pos[0] < 0 or self.matrix.shape[1] - 1 < new_pos[1] or \
                    new_pos[1] < 0:
                continue
            # Cannot go here: too high
            if (self.climbing and self.matrix[new_pos] - 1 > self.matrix[pos]) or \
                    (not self.climbing and self.matrix[new_pos] + 1 < self.matrix[pos]):
                continue

            self.distances_to_start[new_pos] = min(self.distances_to_start[new_pos], current_distance + 1)
        self.visited_nodes[pos] = True
        return not np.any(np.logical_not(self.visited_nodes))

    def dijkstras(self):
        """
        Run Dijkstra's algorithm:
        - Set the current pos to the start pos - For this pos, the min_distance_to_start is known (namely 0)
        - compute_min_distances_to_start_for_neighbors_of for the pos
        - Select the next node: The node with the smallest distance to start, which is unvisited.
            If all nodes are visited, stop.
        """
        pos = self.start_pos
        while not self.compute_min_distances_to_start_for_neighbors_of(pos):
            # Select next node: unvisited and lowest value
            options_next_node = self.distances_to_start.copy()
            options_next_node[self.visited_nodes] = self.max_val
            pos = self.argmin_last_n_axes(options_next_node, 2)
            if self.visited_nodes[pos]:
                break

    @staticmethod
    def argmin_last_n_axes(matrix, n):
        """
        From Stack overflow: For the last n axes of the matrix, find the argmin.
        Hence get the position (only the last n indexes of it) of the cell with the lowest value in matrix
        """
        s = matrix.shape
        new_shp = s[:-n] + (np.prod(s[-n:]),)
        min_idx = matrix.reshape(new_shp).argmin(-1)
        return np.unravel_index(min_idx, s[-n:])

    @property
    def start_pos(self):
        """
        Get the position to start Dijkstras. Is the cell with 0 if climbing, else with self.goal.
        """
        if self.climbing:
            return tuple(np.argwhere(self.matrix == 0)[0])
        else:
            return tuple(np.argwhere(self.matrix == self.goal)[0])


class Puzzle12(PuzzleToSolve):
    @property
    def day(self) -> int:
        return 12

    @property
    def test_input(self) -> str:
        return """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""

    @property
    def test_answer_a(self):
        return 31

    @property
    def test_answer_b(self):
        return 29

    def a(self, input_: str):
        """
        Solve a)
        - Create map
        - Run Dijkstras (climbing)
        - Now get the distance_to_start of the Goal cell (which is thus the distnace of start to gaol)
        """
        map = Map(input_, True)
        map.dijkstras()
        result = map.distances_to_start[tuple(np.argwhere(map.matrix == map.goal)[0])]

        return result

    def b(self, input_: str):
        """
        Solve b)
        - Do so by running an inverse Dijkstras, hence computing the distance to End for all other cells.
        - Replace S with a and E with S. Hence we will start at the end, and there is no goal
        - Create map
        - Run Dijkstras (not climbing). Hence we will run it as decreasing from S to anywhere.
            This will create a map with all shortest distances to S (previous E)
        - Now create the 'options' matrix, which will have the distances_to_start for all cells that have a height of 1.
        - Get the cell with the lowest distance to end, and get its distance
        """
        input_ = input_.replace("S", "a").replace("E", "S")
        map = Map(input_, False)
        map.dijkstras()

        options = map.distances_to_start.copy()
        # All options that are not at height 'a', are not an option. Hence set the distnace to start to max
        options[np.where(map.matrix != 1)] = map.max_val
        # Now for all options, get the one with the lowest distance to start, and get its distance to start
        result = map.distances_to_start[map.argmin_last_n_axes(options, 2)]
        return result


puzzle = Puzzle12()
puzzle.solve()
