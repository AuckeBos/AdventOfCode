from dataclasses import dataclass, field
from typing import List, Tuple

import numpy as np
from numpy.typing import NDArray

from src._2022.puzzle_to_solve import PuzzleToSolve

# Set to True to print matrix configurations during movement application
DEBUG = False


class Rope:
    """
    A Rope is defined by the following attributes:
    Attributes
    ----------
    LETTER_MAPPING: Dict[str, Tuple[int ,int]]
        Static map, maps direction to a tuple indicating the position change on the grid
    knot_count: int
        The number of knots in the rope. Provided in init (2 for a), 10 for b))
    movements: List[Tuple[int ,int]]
        The list of movements to apply. Read from input, each movement is a single step of the first knot
    knot_positions: List[NdArray]
        The position of each knot. Pos is represented as np.array([x, y])
    knot_histories: List[List[Tuple[int, int]]]
        List of knot histories. Indexed by knot index. History is the list of its positions on the grid

    """
    LETTER_MAPPING = {
        'U': (0, -1),
        'L': (-1, 0),
        'D': (0, 1),
        'R': (1, 0),
    }
    knot_count: int
    movements: List[Tuple[int, int]]
    knot_positions: List[NDArray] = None  # List of positions, each position is (x, y). Head is index 0
    knot_histories: List[List[Tuple[int, int]]] = field(default_factory=lambda: [])

    def __init__(self, input_: str, knot_count: int):
        self.knot_count = knot_count
        self.movements = self.parse_input(input_)

    def parse_input(self, input_: str):
        """
        Parse the input:
        - Split on newlines
        - Each line is a movement. Convert each movement to a list of steps. extend tuples
        - Tuples is a list of single step movements.
        """
        lines = input_.split("\n")
        tuples = []
        for line in lines:
            direction, amount = line.split(" ")
            for _ in range(int(amount)):
                tuples.append(self.LETTER_MAPPING[direction])
        return tuples

    def make_knot_follow_successor(self, knot_index: int):
        """
        Make knot knot_index follow its successor:
        - Get successor, and diff of both's x and y
        - If any diff is > 2, raise exception
        - Move x into the right direction, if the diff is 2, or it is 1 and the ydiff is 2
        - Move y into the right direction, if the diff is 2, or it is 1 and the xdiff is 2
        """
        knot_position = self.knot_positions[knot_index]
        successor_position = self.knot_positions[knot_index - 1]
        diff_x, diff_y = successor_position - knot_position

        if abs(diff_x) > 2 or abs(diff_y) > 2:
            raise Exception(f"Something is wrong, The rope snapped at knot {knot_position}")
        x_direction = np.sign(diff_x) if abs(diff_x) == 2 or (abs(diff_x) == 1 and abs(diff_y) == 2) else 0
        y_direction = np.sign(diff_y) if abs(diff_y) == 2 or (abs(diff_y) == 1 and abs(diff_x) == 2) else 0
        self.move_knot(knot_index, (x_direction, y_direction))

    def move_knot(self, index: int, movement: Tuple[int, int]):
        """
        Move a knot: Update self.knot_positions[index] and self.knot_histories[index]
        """
        self.knot_positions[index] += movement
        self.knot_histories[index].append(tuple(self.knot_positions[index]))

    def apply_motions(self):
        """
        Apply the list of motions:
        - Set each knot at start pos
        - Create empty knot histories
        - Iterate over movements:
            - Move the first knot (head)
            - Make all the next knots follow its successor
            - If DEBUG is True, print the current status
        - Return the number of positions that the tail has seen
        """
        self.knot_positions = [np.array([0, 0]) for _ in range(self.knot_count)]
        self.knot_histories = [[(0, 0)] for _ in range(self.knot_count)]
        for i, movement in enumerate(self.movements):
            self.move_knot(0, movement)
            for i in range(1, self.knot_count):
                self.make_knot_follow_successor(i)
            if DEBUG:
                print(self)
                print('')
        result = len(set(self.knot_histories[-1]))
        return result

    def __str__(self):
        """
        Print the current matrix. Will be done during apply_motions, if DEBUG is True.
        - Create empty matrix of 'size'
        - Create empty matrix, where values are '.'
        - Loop over the knot positions. At each pos (+ half size, to prevent negative indexing), set knot name (index)
        - Mark start pos
        - Print matrix as string

        Note: Excepts at some point, as the positions will exceed 'size'. Size can be increased to prevent this,
        however this will decrease readability.
        """
        size = 12
        matrix = np.zeros((size, size)).astype(int).astype(str)
        matrix[matrix == '0'] = '.'
        half = size // 2
        for i, knot in enumerate(self.knot_positions):
            c = knot[0] + half
            r = knot[1] + half
            matrix[r, c] = i
        matrix[half, half] = 's'
        result = []
        for row in matrix:
            result.append(''.join(row))
        return "\n".join(result)


class Puzzle9(PuzzleToSolve):
    @property
    def day(self) -> int:
        return 9

    @property
    def test_input(self) -> str:
        return """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2"""

    @property
    def test_input_alternative(self) -> str:
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

    def a(self, input_: str):
        """
        Solve a):
        - Create a rope with 2 knots
        - Apply the motions
        - Return the result
        """
        rope = Rope(input_, 2)
        result = rope.apply_motions()
        return result

    def b(self, input_: str):
        """
        Solve a):
        - Create a rope with 10 knots
        - Apply the motions
        - Return the result
        """
        rope = Rope(input_, 10)
        result = rope.apply_motions()
        return result


puzzle = Puzzle9()
puzzle.solve()
