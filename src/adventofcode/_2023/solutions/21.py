import numpy as np

from adventofcode._templates.v20231204.puzzle_to_solve import PuzzleToSolve
from adventofcode.helpers.base_matrix_v1 import BaseMatrixV1


class Garden(BaseMatrixV1):
    MAX_VAL = 26501365

    def walk(self, steps: int) -> int:
        test = np.tile(self.data, (steps, steps))
        # Set S to O
        # self.data[self.data == "S"] = "O"
        positions = np.argwhere(self.data == "S").tolist()
        for _ in range(steps):
            new_positions = set()
            while positions:
                i, j = positions.pop()
                neighbors = self.adjacent_fields(i, j, as_values=False, diagonal=False)
                for neighbor in neighbors:
                    if self.data[neighbor] == ".":
                        new_positions.add(neighbor)
            positions = new_positions
            self.print_mat_with_updated_pos(positions)
        return len(positions) + 1

    def print_mat_with_updated_pos(self, positions):
        mat = self.data.copy()
        for i, j in positions:
            mat[i, j] = "O"
        print("\n".join(["".join(line) for line in mat]))


class Puzzle21(PuzzleToSolve):
    @property
    def day(self) -> int:
        return 21

    @property
    def year(self) -> int:
        return 2023

    @property
    def test_input(self) -> str:
        return """...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
..........."""

    @property
    def extra_kwargs(self) -> dict:
        return {
            "a_test": {"steps": 6},
            "b_test": {"steps": 5000},
            "a": {"steps": 64},
            "b": {"steps": 26501365},
        }

    @property
    def test_answer_a(self):
        return 16

    @property
    def test_answer_b(self):
        return 16733044

    def parse_input(self, input_: str) -> Garden:
        garden = Garden()
        garden.parse_input(input_, None)
        return garden

    def a(self, garden: Garden, steps: int):
        return garden.walk(steps)

    def b(self, garden: Garden, steps: int):
        return -1


puzzle = Puzzle21()
puzzle.solve()
