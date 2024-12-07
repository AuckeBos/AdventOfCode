from copy import deepcopy

import numpy as np

from adventofcode._templates.v20231204.puzzle_to_solve import PuzzleToSolve
from adventofcode.helpers.base_matrix import BaseMatrix, Direction, Directions, Position


class Map(BaseMatrix):
    obstructed_position: Position | None = None
    guard_history: list[tuple[Position, Direction]] | None = None
    mask: np.matrix | None = None

    def is_blocked(self, position: Position) -> bool:
        return self[position] == "#" if self.is_in_bounds(position) else False

    @property
    def is_obstructed(self) -> bool:
        return self.obstructed_position is not None

    def obstruct(self, position: Position) -> None:
        self[position] = "#"
        self.obstructed_position = position

    def get_result_by_history(
        self,
        position: Position,
        direction: Direction,
        historical_walks: dict[
            tuple[tuple[int, int], tuple[int, int]], list[tuple[np.matrix, int]]
        ],
    ) -> int | None:
        # When not obstructed, to not use history
        if not self.is_obstructed:
            return False
        # If we have never been here, we can't use history
        if (position.tuple_, direction.tuple_) not in historical_walks:
            return False
        # we have been here
        for mask, result in historical_walks[(position.tuple_, direction.tuple_)]:
            # For this historical run, we have not been at the obstructed position
            # hence, even with the obstruction, the result will be the same as previously
            if mask[*self.obstructed_position.tuple_] != "X":
                if self.obstructed_position.tuple_ in [
                    (6, 3),
                    (6, 7),
                    (6, 8),
                    (8, 1),
                    (8, 3),
                    (9, 7),
                ]:
                    test = ""
                return result
        return None

    def walk_until_exit(
        self,
        position: Position = None,
        direction: Direction = None,
    ) -> int | None:
        position = position or Position(*np.argwhere(self.data == "^")[0])
        direction = direction or Directions.TOP.value
        self.mask = self.data.copy()
        self.guard_history = []
        self.mask[position.tuple_] = "X"
        while self.is_in_bounds(position):
            if (position, direction) in self.guard_history:
                print("Breaking loop")
                return None
            self.mask[*position.tuple_] = "X"
            if self.is_blocked(position + direction):
                direction = direction.turn_right()
            self.guard_history.append((position, direction))
            position += direction
        print("Done")
        return np.count_nonzero(self.mask == "X")


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
        map_count = 0
        original_map = deepcopy(start_map)
        original_map.walk_until_exit()
        original_mask = original_map.mask
        for position in start_map.iter_topleft_to_bottomright():
            # start, or obstruction, or never been in original walk
            if (
                start_map[position] in ["#", "^"]
                or original_mask[position.tuple_] != "X"
            ):
                continue
            if position == Position(1, 4):
                test = ""
            # get the moment in time where we were at this position
            moments_at_position = [
                (i, (p, d))
                for i, (p, d) in enumerate(original_map.guard_history)
                if p == position
            ]
            start_position, start_direction = original_map.guard_history[
                [
                    i
                    for (i, (p, d)) in enumerate(original_map.guard_history)
                    if p == position
                ][0]
                - 1
            ]
            map = deepcopy(start_map)
            map.obstruct(position)
            result = map.walk_until_exit(start_position, start_direction)
            if result is None:
                map_count += 1

        return map_count


puzzle = Puzzle6()
puzzle.solve()
