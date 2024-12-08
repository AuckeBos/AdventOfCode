from copy import deepcopy

import numpy as np
from pqdm.processes import pqdm
from tqdm import tqdm

from adventofcode._templates.v20231204.puzzle_to_solve import PuzzleToSolve
from adventofcode.helpers.base_matrix import BaseMatrix, Direction, Directions, Position


class Map(BaseMatrix):
    obstructed_position: Position | None = None
    guard_history: list[tuple[Position, Direction]] | None = None
    mask: np.matrix | None = None

    DIRECTION_TO_CHAR = {
        Directions.TOP.value: "^",
        Directions.RIGHT.value: ">",
        Directions.BOTTOM.value: "v",
        Directions.LEFT.value: "<",
    }

    def is_blocked(self, position: Position) -> bool:
        return self[position] == "#" if self.is_in_bounds(position) else False

    @property
    def is_obstructed(self) -> bool:
        return self.obstructed_position is not None

    def obstruct(self, position: Position) -> None:
        self[position] = "#"
        self.obstructed_position = position

    def destruct(self, position: Position) -> None:
        self[position] = "."
        self.obstructed_position = None

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
        guard_history: list[tuple[Position, Direction]] = None,
    ) -> int | None:
        position = position or Position(*np.argwhere(self.data == "^")[0])
        direction = direction or Directions.TOP.value
        self.mask = self.data.copy()
        if self.is_obstructed:
            self.mask[*self.obstructed_position.tuple_] = "O"
        self.guard_history = guard_history or []
        while self.is_in_bounds(position):
            if (position, direction) in self.guard_history:
                self.mask[*position.tuple_] = "!"
                # print(self.obstructed_position)
                # print(self.matrix_to_str(self.mask) + "\n\n")
                return None
            self.guard_history.append((position, direction))
            self.mask[*position.tuple_] = self.DIRECTION_TO_CHAR[direction]
            if self.is_blocked(position + direction):
                direction = direction.turn_right()
            position += direction
        return np.count_nonzero(np.isin(self.mask, ["^", ">", "v", "<", "!", "O"]))


def try_one(map: Map, i: int) -> int:
    position_to_block, _ = map.guard_history[i]
    start_position, start_direction = map.guard_history[i - 1]
    # start_direction = start_direction.turn_right()
    map.obstruct(position_to_block)
    result = map.walk_until_exit(
        start_position, start_direction, [*map.guard_history[: i - 1]]
    )
    return 1 if result is None else 0


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

        # for i in tqdm(range(1, len(original_map.guard_history))):
        # start = 4125 if len(original_map.guard_history) > 4120 else 1
        start = 1
        args = []
        tried = []
        for i in range(start, len(original_map.guard_history)):
            position = original_map.guard_history[i][0]
            if position in tried:
                continue
            tried.append(position)
            args.append((original_map, i))

        result = pqdm(args, try_one, n_jobs=15, argument_type="args")

        return sum(result)

        for i in tqdm(range(start, len(original_map.guard_history))):
            # for i in range(start, len(original_map.guard_history)):
            # print(
            #     f"{i}/{len(original_map.guard_history)} ({i/len(original_map.guard_history)*100:.2f}%)",
            #     end="\r",
            # )
            position_to_block, _ = original_map.guard_history[i]
            start_position, start_direction = original_map.guard_history[i - 1]
            start_direction = start_direction.turn_right()
            if start_position == Position(1, 4):
                test = ""
            # map = deepcopy(start_map)
            start_map.obstruct(position_to_block)
            result = start_map.walk_until_exit(
                start_position, start_direction, [*original_map.guard_history[: i - 1]]
            )
            if result is None:
                map_count += 1
            start_map.destruct(position_to_block)

        return map_count


if __name__ == "__main__":
    puzzle = Puzzle6()
    puzzle.solve()
