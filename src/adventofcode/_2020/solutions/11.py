import numpy as np

from adventofcode._templates.v20231204.puzzle_to_solve import PuzzleToSolve
from adventofcode.helpers.base_matrix_v1 import BaseMatrixV1


class Matrix(BaseMatrixV1):
    def simulate(self, look_far: bool = False):
        tolerance = 4 if not look_far else 5
        new_data = self.data.copy()
        for i, j in self.iter_topleft_to_bottomright():
            if look_far:
                neighbors = self.get_visible_seats(i, j)
            else:
                neighbors = self.adjacent_fields(i, j, as_values=True)
            if self.data[i, j] == "L" and "#" not in neighbors:
                new_data[i, j] = "#"
            if self.data[i, j] == "#" and neighbors.count("#") >= tolerance:
                new_data[i, j] = "L"
        if not np.array_equal(self.data, new_data):
            self.data = new_data
            self.simulate(look_far)

    def occupied_seats(self):
        return np.count_nonzero(self.data == "#")

    def get_visible_seat(self, i, j, direction):
        i += direction[0]
        j += direction[1]
        while 0 < i < self.data.shape[0] - 1 and 0 < j < self.data.shape[1] - 1:
            if self.data[i, j] in ["L", "#"]:
                return self.data[i, j]
            i += direction[0]
            j += direction[1]
        return None

    def get_visible_seats(self, i, j):
        visible_seats = []
        for direction in [
            (1, 0),
            (0, 1),
            (-1, 0),
            (0, -1),
            (1, -1),
            (-1, 1),
            (1, 1),
            (-1, -1),
        ]:
            visible_seat = self.get_visible_seat(i, j, direction)
            if visible_seat:
                visible_seats.append(visible_seat)
                continue
        return visible_seats


class Puzzle11(PuzzleToSolve):
    @property
    def day(self) -> int:
        return 11

    @property
    def year(self) -> int:
        return 2020

    @property
    def test_input(self) -> str:
        return """L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL"""

    @property
    def test_answer_a(self):
        return 37

    @property
    def test_answer_b(self):
        return 26

    def parse_input(self, input_: str) -> Matrix:
        matrix = Matrix()
        matrix.parse_input(input_)
        return matrix

    def a(self, matrix: Matrix):
        matrix.simulate()
        return matrix.occupied_seats()

    def b(self, matrix: Matrix):
        matrix.simulate(look_far=True)
        return matrix.occupied_seats()


puzzle = Puzzle11()
puzzle.solve()
