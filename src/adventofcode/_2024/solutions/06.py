from collections import defaultdict

import numpy as np
from tqdm import tqdm

from adventofcode._templates.v20231204.puzzle_to_solve import PuzzleToSolve
from adventofcode.helpers.base_matrix import BaseMatrix, Direction, Directions, Position


class InfiniteLoopError(Exception):
    def __init__(self):
        super().__init__("Guard stuck in loop")


class Map(BaseMatrix):
    def __init__(self, input_: str):
        super().__init__(input_, None, str)

    def is_blocked(self, position: Position) -> bool:
        return self[position] == "#" if self.is_in_bounds(position) else False

    def walk_until_exit(self) -> dict[Position, list[Direction]]:
        """
        Walk the map until the guard would exit the map. Return the history of the guard's path
        Raise InfiniteLoopError if the guard would loop
        """
        position = Position(*np.argwhere(self.data == "^")[0])
        direction = Directions.TOP.value
        guard_history = defaultdict(set)
        # Until the guard would exit the map in the next step
        while self.is_in_bounds(position + direction):
            guard_history[position].add(direction)
            if self.is_blocked(position + direction):
                direction = direction.turn_right()
                continue
            # Deja vu
            if direction in guard_history[position + direction]:
                raise InfiniteLoopError
            position += direction

        return guard_history


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
        return Map(input_)

    def a(self, map_: Map) -> int:
        return len(map_.walk_until_exit())

    def b(self, map_: Map) -> int:
        result = 0
        guard_history = map_.walk_until_exit()
        start = Position(*np.argwhere(map_.data == "^")[0])
        for position in tqdm(guard_history.keys()):
            if position == start:
                continue
            map_[position] = "#"
            try:
                map_.walk_until_exit()
            except InfiniteLoopError:
                result += 1
            finally:
                map_[position] = "."
        return result


if __name__ == "__main__":
    puzzle = Puzzle6()
    puzzle.solve()
