from typing import List, Tuple

import numpy as np
from numpy import ndarray

from adventofcode._templates.v20231204.puzzle_to_solve import PuzzleToSolve
from adventofcode.helpers.base_matrix_v1 import BaseMatrixV1


class Lagoon(BaseMatrixV1):
    data: ndarray
    lines: List[Tuple[str, int, str]]

    dir_to_tuple = {"R": (0, 1), "L": (0, -1), "U": (-1, 0), "D": (1, 0)}

    def __init__(self, lines: List[Tuple[str, int, str]]):
        self.pad = None
        self.lines = lines
        self.data = np.full((2000, 2000), fill_value=".", dtype=str)

    def dig_plan(self):
        loc = (1000, 1000)
        corners = [(0, 0)]
        for direction, amount, _ in self.lines:
            dir_tuple = self.dir_to_tuple[direction]
            original_new_loc = (
                loc[0] + dir_tuple[0] * amount,
                loc[1] + dir_tuple[1] * amount,
            )
            loc, new_loc = sorted([loc, original_new_loc])
            self.data[loc[0] : new_loc[0] + 1, loc[1] : new_loc[1] + 1] = "#"
            loc = original_new_loc
            # corners.append((loc[0]:new_loc[0] + 1, loc[1]:new_loc[1] + 1)))
            # print(self)
        # decrease self.data, with the max # on row and column
        self.data = self.data[
            np.min(np.argwhere(self.data == "#")[:, 0]) : np.max(
                np.argwhere(self.data == "#")[:, 0]
            )
            + 1,
            np.min(np.argwhere(self.data == "#")[:, 1]) : np.max(
                np.argwhere(self.data == "#")[:, 1]
            )
            + 1,
        ]
        print(self)
        self.corners = np.array(corners)
        test = ""

    def calculate_area(self):
        points = np.argwhere(self.data == "#")
        x = points[:, 0]
        y = points[:, 1]
        return 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))

    def fill_loop_old(self):
        """
        Use the crossing number method to figure out the area in the loop
        For each field, draw a line from the left of the row untill the field (if the field is not part of the loop itself)
        Toggle the boolean is_in_the loop for each # we encounter
        Skip successive #'s, because we are on the border of the loop
        """
        new_data = self.data.copy()
        for r, c in self.iter_topleft_to_bottomright():
            if self.data[r, c] == "#":
                continue
            # Check if at least one # on the left
            if "#" in self.data[r, :c] and "#" in self.data[r, c:]:
                new_data[r, c] = "#"
        self.data = new_data
        print(self)
        return np.count_nonzero(self.data == "#")

    def find_point_in_loop(self):
        """
        Find a point that is in the loop
        """
        # We know that 1000, 1000 is a corner.
        if self.data[1000, 1001] == "#" and self.data[1001, 1000] == "#":
            return 1001, 1001
        if self.data[1000, 999] == "#" and self.data[1001, 1000] == "#":
            return 1001, 999
        if self.data[1000, 1001] == "#" and self.data[999, 1000] == "#":
            return 999, 1001
        if self.data[1000, 999] == "#" and self.data[999, 1000] == "#":
            return 999, 999

    def flood_fill(self, start):
        data = self.data
        stack = [start]
        while stack:
            x, y = stack.pop()
            if data[x, y] == ".":
                data[x, y] = "#"
                if x > 0:
                    stack.append((x - 1, y))
                if x < data.shape[0] - 1:
                    stack.append((x + 1, y))
                if y > 0:
                    stack.append((x, y - 1))
                if y < data.shape[1] - 1:
                    stack.append((x, y + 1))
        self.data = data
        print(self)

    def fill_outside_loop(self):
        # pad self.data
        corner_count = np.count_nonzero(self.data == "#")
        self.data = np.pad(self.data, 1, mode="constant", constant_values=".")
        self.flood_fill((0, 0))
        inner_count = np.count_nonzero(self.data == ".")
        return corner_count + inner_count


class Puzzle18(PuzzleToSolve):
    @property
    def day(self) -> int:
        return 18

    @property
    def year(self) -> int:
        return 2023

    @property
    def test_input(self) -> str:
        return """R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)"""

    @property
    def test_answer_a(self):
        return 62

    @property
    def test_answer_b(self):
        return None

    def parse_input(self, input_: str) -> Lagoon:
        lines = input_.splitlines()
        lines = [line.split(" ") for line in lines]
        lines = [(line[0], int(line[1]), line[2].strip("()")) for line in lines]
        return Lagoon(lines)

    def calculate_area(self, corners):
        corners = corners.reshape(-1, 2)
        x = corners[:, 0]
        y = corners[:, 1]
        return 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))

    def a(self, lagoon: Lagoon):
        lagoon.dig_plan()
        return lagoon.fill_outside_loop()
        fill_count = self.calculate_area(lagoon.corners)
        corner_count = np.count_nonzero(lagoon.data == "#")
        result = fill_count + corner_count
        return result
        # result = lagoon.fill_outside_loop()
        # return result

    def b(self, lagoon: Lagoon):
        dirs = ["R", "D", "L", "U"]
        colors = [color for _, _, color in lagoon.lines]
        converted = []
        for color in colors:
            amount = int(color[:5])

        return -1


puzzle = Puzzle18()
puzzle.solve()
