from dataclasses import dataclass, field
from typing import List, Tuple

import numpy as np
from numpy.typing import NDArray

from src._2022.puzzle_to_solve import PuzzleToSolve

@dataclass
class SmallRope:
    letter_mapping = {
        'U': (0, -1),
        'L': (-1, 0),
        'D': (0, 1),
        'R': (1, 0),
    }

    input: str
    head_pos: NDArray = None
    tail_pos: NDArray = None
    tail_history: List[Tuple[int, int]] = field(default_factory=lambda: [])

    def parse_input(self):
        lines = self.input.split("\n")
        tuples = []
        for line in lines:
            direction, amount = line.split(" ")
            for _ in range(int(amount)):
                tuples.append(self.letter_mapping[direction])
        return tuples


    def move_tail(self, item: Tuple[int, int]):
        self.tail_pos += item
        self.tail_history.append(tuple(self.tail_pos))

    def make_tail_follow_head(self):
        diff_x, diff_y = self.head_pos - self.tail_pos
        if diff_x == 0 or abs(diff_x) == 1:
            pass
        elif abs(diff_x) == 2:
            # Then move horizontally
            if diff_y == 0:
                direction = 1 if diff_x > 0 else -1
                self.move_tail((direction, 0))
            # Move diagonally
            else:
                x_direction = 1 if diff_x > 0 else -1
                y_direction = 1 if diff_y > 0 else -1
                self.move_tail((x_direction, y_direction))
        else:
            raise Exception(f"Invalid position of head: It is more than 2 spaces apart horizontally")

        if diff_y == 0 or abs(diff_y) == 1:
            pass
        elif abs(diff_y) == 2:
            # Then move vertically
            if diff_x == 0:
                direction = 1 if diff_y > 0 else -1
                self.move_tail((0, direction))
            # Move diagonally
            else:
                x_direction = 1 if diff_x > 0 else -1
                y_direction = 1 if diff_y > 0 else -1
                self.move_tail((x_direction, y_direction))
        else:
            raise Exception(f"Invalid position of head: It is more than 2 spaces apart vertically")

    def move_head(self, tuple: Tuple[int, int]):
        self.head_pos += tuple

    def apply_motions(self):
        self.head_pos = np.array([0,0])
        self.tail_pos = np.array([0,0])
        self.tail_history.append(tuple(self.tail_pos))
        tuples = self.parse_input()
        for item in tuples:
            self.move_head(item)
            self.make_tail_follow_head()
        result = len(set(self.tail_history))
        return result

@dataclass
class LargeRope:
    letter_mapping = {
        'U': (0, -1),
        'L': (-1, 0),
        'D': (0, 1),
        'R': (1, 0),
    }

    input: str
    knot_positions: List[NDArray] = None # List of positions, each position is (x, y). Head is index 0
    knot_histories: List[List[Tuple[int, int]]] = field(default_factory=lambda: [])

    def parse_input(self):
        lines = self.input.split("\n")
        tuples = []
        for line in lines:
            direction, amount = line.split(" ")
            for _ in range(int(amount)):
                tuples.append(self.letter_mapping[direction])
        return tuples

    def make_knot_follow_successor(self, knot_index: int):
        knot_position = self.knot_positions[knot_index]
        successor_position = self.knot_positions[knot_index - 1]

        diff_x, diff_y = successor_position - knot_position
        if diff_x == 0 or abs(diff_x) == 1:
            pass
        elif abs(diff_x) == 2:
            # Then move horizontally
            if diff_y == 0:
                direction = 1 if diff_x > 0 else -1
                self.move_knot(knot_index, (direction, 0))
            # Move diagonally
            else:
                x_direction = 1 if diff_x > 0 else -1
                y_direction = 1 if diff_y > 0 else -1
                self.move_knot(knot_index, (x_direction, y_direction))
        else:
            pass
        if diff_y == 0 or abs(diff_y) == 1:
            pass
        elif abs(diff_y) == 2:
            # Then move vertically
            if diff_x == 0:
                direction = 1 if diff_y > 0 else -1
                self.move_knot(knot_index, (0, direction))
            # Move diagonally
            else:
                x_direction = 1 if diff_x > 0 else -1
                y_direction = 1 if diff_y > 0 else -1
                self.move_knot(knot_index, (x_direction, y_direction))
        else:
            pass
            # raise Exception(f"Invalid position of head: It is more than 2 spaces apart vertically")

    def move_knot(self, index: int, movement: Tuple[int, int]):
        self.knot_positions[index] += movement
        self.knot_histories[index].append(tuple(self.knot_positions[index]))



    def apply_motions(self):
        self.knot_positions = [np.array([0,0]) for _ in range(10)]
        self.knot_histories = [[(0,0)] for _ in range(10)]
        movements = self.parse_input()
        for i, movement in enumerate(movements):
            self.move_knot(0, movement)
            for i in range(1, 10):
                self.make_knot_follow_successor(i)
        result = len(set(self.knot_histories[9])) - 1
        return result



class Puzzle9(PuzzleToSolve):
    @property
    def day(self) -> int:
        return 9

    @property
    def test_input(self) -> str:
        return """R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20"""

    @property
    def test_answer_a(self):
        return 13

    @property
    def test_answer_b(self):
        return 36

    def a(self, input: str):
        rope = SmallRope(input)
        result = rope.apply_motions()
        return result

    def b(self, input: str):
        rope = LargeRope(input)
        result = rope.apply_motions()
        return result


puzzle = Puzzle9()
puzzle.solve()
