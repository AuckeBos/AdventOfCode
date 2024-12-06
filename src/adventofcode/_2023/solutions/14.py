import numpy as np
from numpy import ndarray

from adventofcode._templates.v20231204.puzzle_to_solve import PuzzleToSolve
from adventofcode.helpers.base_matrix_v1 import BaseMatrixV1

# def


class Dish(BaseMatrixV1):
    encountered_patterns: dict

    def spin(self, times: int):
        """
        Spin the dish a number of times.
        After each spin, check whether the pattern has been encountered before. If so, we can skip cycles.
        """
        self.encountered_patterns = {}
        i = 0
        while i < times:
            self.spin_once()
            new_i = self.try_skip_cycles(i)
            self.encountered_patterns[self.__repr__()] = i
            i = new_i

    def try_skip_cycles(self, i: int):
        """
        Check if the current pattern has been encountered before. If so, we can skip cycles.
        """
        if self.__repr__() in self.encountered_patterns:
            # Find the length of the repeating pattern
            length_of_repeating_pattern = i - self.encountered_patterns[self.__repr__()]
            # Skip as many times as the length fits in the remaining cycles
            remaining_cycles = 1000000000 - i
            i = 1000000000 - (remaining_cycles % length_of_repeating_pattern)
        return i + 1

    def spin_once(self):
        for direction in ["north", "west", "south", "east"]:
            self.tilt_dish(direction)

    def tilt_dish(self, direction: str):
        """
        Tilt the dish in a direction.
        First get the cols, based on the direction. Then tilt each col, and glue back together.
        Todo: Generalize
        """
        if direction == "north":
            cols = self.data.T
        if direction == "west":
            cols = self.data
        if direction == "south":
            cols = [c[::-1] for c in self.data.T]
        if direction == "east":
            cols = [c[::-1] for c in self.data]
        tilted = np.array([self.tilt_range(c) for c in cols])
        if direction == "north":
            tilted = tilted.T
        if direction == "south":
            tilted = np.rot90(tilted, 1)
        if direction == "east":
            tilted = np.flip(tilted, axis=1)

        self.data = tilted

    def tilt_range(self, _range: ndarray) -> ndarray:
        """
        Tilt one range (col or row), to move all the round rocks to the left.

        Args:
            _range: The range to tilt.
        Returns:
            The tilted range. (All rounded rocks moved to the left, untill start or cube rock)
        """
        new_range = []
        free_space_count = 0
        for pos in _range:
            # If we ecounter a cube rock, all free spaces will not be filled with round rocks. Append the free spaces and the cube rock.
            if pos == "#":
                new_range.extend("." * free_space_count)
                free_space_count = 0
                new_range.append(pos)
            if pos == "O":
                # Simply add it. If have free space, it will be added with the next cube rock.
                new_range.append(pos)
            if pos == ".":
                # Add the free space to the count, will be added upon the next cube rock.
                free_space_count += 1
        # Append the remaining free space
        if free_space_count > 0:
            new_range.extend("." * free_space_count)
        return np.array(new_range)

    def compute_load(self):
        """
        Sum the load for each round rock. For each round rock its the nr of rows minus the row index.
        """
        return np.sum(
            self.data.shape[0] - r
            for r, c in self.iter_topleft_to_bottomright()
            if self.data[r, c] == "O"
        )

    def __repr__(self):
        return "\n".join(["".join(row) for row in self.data])

    def __hash__(self):
        return hash(self.__repr__())


class Puzzle14(PuzzleToSolve):
    @property
    def day(self) -> int:
        return 14

    @property
    def year(self) -> int:
        return 2023

    @property
    def test_input(self) -> str:
        return """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#...."""

    @property
    def test_answer_a(self):
        return 136

    @property
    def test_answer_b(self):
        return 64

    def parse_input(self, input_: str) -> Dish:
        dish = Dish()
        dish.parse_input(input_, None)
        return dish

    def a(self, dish: Dish) -> int:
        """
        Tilt the dish to the north, and compute the load.
        """
        dish.tilt_dish("north")
        return dish.compute_load()

    def b(self, dish: Dish) -> int:
        """
        Spin the dish a billion times, and compute the load.
        """
        dish.spin(1000000000)
        return dish.compute_load()


puzzle = Puzzle14()
puzzle.solve()
