import numpy as np

from adventofcode._templates.v20231204.puzzle_to_solve import PuzzleToSolve
from adventofcode.helpers.base_matrix_v1 import BaseMatrixV1


class Matrix(BaseMatrixV1):
    distances: np.ndarray

    def find_loop(self):
        """
        Start at the start
        Find all adjacent fields that are connected
        Set the distance, and continue to the next
        Stop when back at start.
        We now have a matrix with the distances from the start, given we move into one random direction
        """
        start = self.get_start()
        prev_pos, current_pos = start, start
        distances = np.zeros(self.data.shape)
        current_distance = 0
        back_at_start = False
        while not back_at_start:
            adjacent_fields = self.adjacent_fields(
                *current_pos, as_values=False, diagonal=False
            )
            for new_pos in adjacent_fields:
                # Prevent going back
                if new_pos == prev_pos:
                    continue
                if self.is_connected(*current_pos, *new_pos):
                    distances[new_pos] = current_distance + 1
                    current_distance += 1
                    prev_pos = current_pos
                    current_pos = new_pos
                    if self.data[current_pos] == "S":
                        back_at_start = True
                    break
            else:
                raise ValueError(
                    f"No adjacent fields found for {current_pos} ({self.data[current_pos]})"
                )
        self.distances = distances

    def get_start(self):
        """
        Find the start position
        """
        start = np.where(self.data == "S")
        return start[0][0], start[1][0]

    def max_distance(self):
        """
        After the loop is found, the shortest distance is the max distance divided by 2 (since we move in one direction)
        """
        max_distance = int(np.max(self.distances) / 2)
        return max_distance

    def is_part_of_loop(self, r, c):
        """
        Check if a position is a pipe of the loop
        """
        return self.distances[r, c] > 0

    def replace_start(self):
        """
        Replace the S with the correct pipe:
        Find the neighbors of the start (distance 1 or max - 1)
        Replace S with a pipe, check if the neighbors are still connected. If so, we found the correct pipe. Else try another one
        """
        start = self.get_start()
        neighbors = list(
            zip(
                *np.where(
                    np.logical_or(
                        self.distances == 1,
                        self.distances == np.max(self.distances) - 1,
                    )
                )
            )
        )
        for char in ["L", "J", "7", "F", "|", "-"]:
            self.data[start] = char
            for pos in neighbors:
                if self.is_connected(*pos, *start):
                    continue
                else:
                    break
            else:
                return

    def calculate_area_in_loop(self):
        """
        Use the crossing number method to figure out the area in the loop
        Replace start, to close the loop
        For each field, draw a line from the left of the row untill the field (if the field is not part of the loop itself)
        Toggle the boolean is_in_the loop for each |, 7, F we encounter (Exclude L and J, because it would be succeeded by -'s, untill a 7 respectively F is encountered)
        If the toggle is true when we reach the field, it is part of the loop, else it is not
        """
        self.replace_start()
        area_count = 0
        for r, c in self.iter_topleft_to_bottomright():
            if self.is_part_of_loop(r, c):
                continue
            in_the_loop = False
            for i in range(c):
                if self.is_part_of_loop(r, i):
                    in_the_loop = (
                        not in_the_loop
                        if self.data[r, i] in ["|", "7", "F"]
                        else in_the_loop
                    )
            if in_the_loop:
                area_count += 1
        return area_count

    def is_connected(self, r_1: int, c_1: int, r_2: int, c_2: int) -> bool:
        """
        Check if two fields are connected to each other.
        Hardcode all the valid combinations of pipes
        """
        v_1, v_2 = self.data[r_1, c_1], self.data[r_2, c_2]
        if v_1 == ".":
            return False
        # If we encounter the start, we can just reverse the arguments
        if v_1 == "S":
            return self.is_connected(r_2, c_2, r_1, c_1)
        if v_1 == "|":
            return c_1 == c_2 and (
                (r_2 == r_1 + 1 and v_2 in ["|", "L", "J", "S"])
                or (r_2 == r_1 - 1 and v_2 in ["|", "7", "F", "S"])
            )
        if v_1 == "-":
            return r_1 == r_2 and (
                (c_2 == c_1 + 1 and v_2 in ["-", "7", "J", "S"])
                or (c_2 == c_1 - 1 and v_2 in ["-", "L", "F", "S"])
            )
        if v_1 == "L":
            return (c_2 == c_1 + 1 and r_2 == r_1 and v_2 in ["-", "7", "J", "S"]) or (
                c_2 == c_1 and r_2 == r_1 + -1 and v_2 in ["|", "7", "F", "S"]
            )
        if v_1 == "J":
            return (c_2 == c_1 - 1 and r_2 == r_1 and v_2 in ["-", "L", "F", "S"]) or (
                c_2 == c_1 and r_2 == r_1 - 1 and v_2 in ["|", "F", "7", "S"]
            )
        if v_1 == "7":
            return (c_2 == c_1 - 1 and r_2 == r_1 and v_2 in ["-", "L", "F", "S"]) or (
                c_2 == c_1 and r_2 == r_1 + 1 and v_2 in ["|", "L", "J", "S"]
            )
        if v_1 == "F":
            return (c_2 == c_1 + 1 and r_2 == r_1 and v_2 in ["-", "7", "J", "S"]) or (
                c_2 == c_1 and r_2 == r_1 + 1 and v_2 in ["|", "J", "L", "S"]
            )
        raise ValueError(f"Unknown value {v_1} at {c_1}, {r_1}")


class Puzzle10(PuzzleToSolve):
    @property
    def day(self) -> int:
        return 10

    @property
    def year(self) -> int:
        return 2023

    @property
    def test_input(self) -> str:
        return """7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ"""

    @property
    def test_input_alternative(self) -> str:
        return """.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ..."""

    @property
    def test_answer_a(self):
        return 8

    @property
    def test_answer_b(self):
        return 10

    def parse_input(self, input_: str):
        matrix = Matrix()
        matrix.parse_input(input_)
        return matrix

    def a(self, matrix: Matrix):
        """
        Find the loop, and calculate the max distance
        """
        matrix.find_loop()
        return matrix.max_distance()

    def b(self, matrix: Matrix):
        """
        Find the loop, and calculate the area in the loop
        """
        matrix.find_loop()
        return matrix.calculate_area_in_loop()


puzzle = Puzzle10()
puzzle.solve()
