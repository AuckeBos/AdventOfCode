from copy import deepcopy

import numpy as np

from adventofcode._templates.v20231204.puzzle_to_solve import PuzzleToSolve
from adventofcode.helpers.base_matrix import BaseMatrix, Direction, Directions, Position


class Map(BaseMatrix):
    def is_blocked(self, position: Position) -> bool:
        return self[position] == "#" if self.is_in_bounds(position) else False

    def walk_until_exit(self) -> int | None:
        position = Position(*np.argwhere(self.data == "^")[0])
        mask = self.data.copy()
        guard_history: list[tuple[Position, Direction]] = []
        mask[mask == "^"] = "X"
        direction = Directions.TOP.value
        while self.is_in_bounds(position):
            if (position, direction) in guard_history:
                print("Breaking loop")
                return None
            guard_history.append((position, direction))
            mask[*position.tuple_] = "X"
            if self.is_blocked(position + direction):
                direction = direction.turn_right()
            position += direction
        print("Done")
        return np.count_nonzero(mask == "X")


class Puzzle6(PuzzleToSolve):
    @property
    def day(self) -> int:
        return 6

    @property
    def year(self) -> int:
        return 2024

    @property
    def test_input(self) -> str:
        return """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""

    @property
    def test_answer_a(self):
        return 41

    @property
    def test_answer_b(self):
        return 6

    def parse_input(self, input_: str) -> Map:
        return Map(input_, pad=None, dtype=str)

    def a(self, map: Map) -> int:
        return map.walk_until_exit()

    def b(self, start_map: Map) -> int:
        print("Starting b")
        result = 0
        for position in start_map.iter_topleft_to_bottomright():
            if start_map[position] in ["#", "^"]:
                continue
            map = deepcopy(start_map)
            map[position] = "#"
            if map.walk_until_exit() is None:
                result += 1
        return result


puzzle = Puzzle6()
puzzle.solve()
