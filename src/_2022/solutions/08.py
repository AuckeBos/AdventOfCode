from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from src._2022.puzzle_to_solve import PuzzleToSolve
import re


@dataclass
class Grid:
    input: str
    matrix: NDArray = None

    def parse_input(self):
        """
        Parse the matrix input:
        - Replace each digit {d} with {d},
        - Replace \n with ;
        - Now np.matrix() creates the matrix as expected
        """
        input = re.sub('(\d)', '\\1,', self.input)
        input = input.replace("\n", ";")
        self.matrix = np.array(np.matrix(input))

    def get_best_tree(self):
        """
        Get the tree with the highest scening score:
        - Loop over each tree, for each tree compute the scenic score by multiplying:
            - Look left: If at left, 0. Else find the most right treeI that is higher then self, return selfI
                (the viewing distance). If not found, the most right tree is at 0, hence distance is selfI
            - Look right: if at right, 0. Else find most left tree that is higher then self
                (add j+1, since index is only over the sublist, hence increase with len of part before sublist). If not
                found return max_j (most right tree). View is the found treeI - selfI.
            - Look up similar to left
            - Look down similar to right
        - Return the max scenic view
        """
        scening_scores = np.zeros(self.matrix.shape, dtype=int)
        max_i = self.matrix.shape[0] - 1
        max_j = self.matrix.shape[1] - 1
        for i in range(self.matrix.shape[0]):
            for j in range(self.matrix.shape[1]):
                tree_len = self.matrix[i, j]
                scening_scores[i, j] = (
                    # Look left
                        (0 if j == 0 else j - max(np.argwhere(self.matrix[i, :j] >= tree_len), default=0)) *
                        # Look right
                        (0 if j == max_j else min(np.argwhere(self.matrix[i, j + 1:] >= tree_len) + j + 1,
                                                  default=max_j) - j) *
                        # Look up
                        (0 if i == 0 else i - max(np.argwhere(self.matrix[:i, j] >= tree_len), default=0)) *
                        # Look down
                        (0 if i == max_i else min(np.argwhere(self.matrix[i + 1:, j] >= tree_len) + i + 1,
                                                  default=max_i) - i)
                )

        return np.max(scening_scores)

    def count_trees(self):
        """
        Count trees that are visible from outside the map:
        - Loop over all trees. For each tree, check whether it is visible by:
            - If is at outer, yes
            - Else if all to the [left|right|up|down] are smaller, yes
        - Return the sum of the treest that are visible
        """
        visible_trees = np.zeros(self.matrix.shape, dtype=bool)
        max_i = self.matrix.shape[0] - 1
        max_j = self.matrix.shape[1] - 1
        for i in range(self.matrix.shape[0]):
            for j in range(self.matrix.shape[1]):
                tree_len = self.matrix[i, j]
                visible_trees[i, j] = (
                        i == 0 or j == 0 or i == max_i or j == max_j or # Outer
                        max(self.matrix[i, :j]) < tree_len or # Look left
                        max(self.matrix[i, j + 1:]) < tree_len or # Look right
                        max(self.matrix[:i, j]) < tree_len or # Look up
                        max(self.matrix[i + 1:, j]) < tree_len # Look down

                )
        return np.count_nonzero(visible_trees)


class Puzzle8(PuzzleToSolve):
    @property
    def day(self) -> int:
        return 8

    @property
    def test_input(self) -> str:
        return """30373
25512
65332
33549
35390"""

    @property
    def test_answer_a(self):
        return 21

    @property
    def test_answer_b(self):
        return 8

    def a(self, input: str):
        """
        Solve a):
        Create grid, parse input, count trees
        """
        grid = Grid(input)
        grid.parse_input()
        result = grid.count_trees()
        return result

    def b(self, input: str):
        """
        Solve b):
        Create grid, parse input, get best tree
        """
        grid = Grid(input)
        grid.parse_input()
        result = grid.get_best_tree()
        return result


puzzle = Puzzle8()
puzzle.solve()
