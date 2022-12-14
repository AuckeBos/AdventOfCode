import numpy as np
from numpy.typing import NDArray

from helpers import xys_to_rcs
from src._2022.puzzle_to_solve import PuzzleToSolve


class Cave:
    """
    Attributes
    ----------
    CAVE_SIZE: Tuple[int, int]
        The size of the cave, format rowcount,columncount
    bottom: int
        The row that contains the most bottom rock (eg height y/r with at least one rock)
    cave: NDArray
        The cave possitions. Values are:
        0: Free
        1: Rock
        2: Sand
    is_endless: bool
        True for a), false for b). If False, one row of stone is added at self.bottom + 2.
        Then the bottom is increased by 2. When the cave is filled, a drop never enters the void, and we stop
        whenever a drop is placed in the entrypoint
    """

    CAVE_SIZE = (1000, 1000)
    bottom: int
    cave: NDArray
    is_endless: bool

    RELATIVE_POSITIONS = (np.array([1, 0]), np.array([1, -1]), np.array([1, 1]))

    def __init__(self, inpt: str, is_endless=True):
        self.is_endless = is_endless
        self.parse_input(inpt)

    def parse_input(self, inpt: str):
        """
        Parse the input string into self.cave:
        - Convert input to a list of endpoints
        - For each tuple of endpoints, get the r,c ranges, and set self.cave to 1 on these locations
        - Set self.bottom to the lowest row with at least 1 stone
        - If the cave is not endless (in b)), increase bottom by 2, and place stones at the bottom row
        """
        matrix = np.zeros(self.CAVE_SIZE, dtype=int)
        lines = [[endpoint.split(',') for endpoint in line.split(' -> ')] for line in inpt.split("\n")]
        for line in lines:
            for i in range(len(line) - 1):
                start, end = line[i], line[i + 1]
                r, c = xys_to_rcs(*start, *end)
                matrix[r, c] = 1
        self.bottom = max(np.argwhere(matrix.any(axis=1)))[0]
        if not self.is_endless:
            self.bottom += 2
            matrix[self.bottom, :] = 1
        self.cave = matrix

    def drop_sand(self, pos):
        """
        Drop a unit of send at pos:
        - If the cave is not empty at this pos (eg there is a stone or sand), return False: We cannot drop the sand
        - If the position is below the bottom, we are in the void,
            hence return false: We cannot drop the sand                                 .
        - Else, get the three options in the right order, and iteration. Options are:  123
            - If the option is an empty positon, recurse drop_sand in that position, and return            .
        - If none of the options are empty position, drop the sand in the current position. We are in pos ###

        """
        # If the position is yet filled, or this position is in the void
        if self.cave[pos] != 0 or pos[0] >= self.bottom:
            return False
        options = [tuple(pos + relative_pos) for relative_pos in self.RELATIVE_POSITIONS]
        for option in options:
            # If option is empty, drop the sand there
            if self.cave[option] == 0:
                return self.drop_sand(option)
        else:  # All positions are blocked, drop in self
            self.cave[pos] = 2
            return True

    def fill(self):
        """
        Fill the cave one at a time, at the entrypoint. Stop as soon as the first drop enters the void,
        or, in the case of a non-endless cave, when the drop fills the endtrypoint of the cave (eg the cave is full)
        """
        while self.drop_sand((0, 500)):
            pass
        return

    @property
    def amount_of_sand(self):
        """
        Return the amount of sand drops in this cave
        """
        return np.count_nonzero(self.cave == 2)


class Puzzle14(PuzzleToSolve):
    @property
    def day(self) -> int:
        return 14

    @property
    def test_input(self) -> str:
        return """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9"""

    @property
    def test_answer_a(self):
        return 24

    @property
    def test_answer_b(self):
        return 93

    def a(self, input: str):
        """
        Solve a):
        - Create an endless cave
        - Fill it
        - Return the amount of sand drops
        """
        cave = Cave(input, True)
        cave.fill()
        result = cave.amount_of_sand
        return result

    def b(self, input: str):
        """
        Solve a):
        - Create a non-endless cave
        - Fill it
        - Return the amount of sand drops
        """
        cave = Cave(input, False)
        cave.fill()
        result = cave.amount_of_sand
        return result


puzzle = Puzzle14()
puzzle.solve()
