from copy import copy, deepcopy
from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from src._2022.puzzle_to_solve import PuzzleToSolve


@dataclass
class Position:
    left: int
    right: int
    top: int
    bottom: int

    previous: 'Position' = None

    def apply(self, gas):
        self.previous = copy(self)
        if gas == '>':
            if self.right < 7:
                self.left += 1
                self.right += 1
        elif gas == '<':
            if self.left > 0:
                self.left -= 1
                self.right -= 1
        else:
            raise Exception(f"Invalid gas type {gas}")
        return self

    def lower(self):
        self.previous = copy(self)
        self.top += 1
        self.bottom += 1
        return self

    def for_numpy(self):
        return range(self.left, self.right + 1), range(self.top, self.bottom + 1)

    def revert(self):
        return self.previous


class Chamber:
    WIDTH = 7
    space = np.zeros((0, WIDTH), dtype=int)

    rocks = [
        np.matrix("1 1 1 1"),
        np.matrix("0 2 0; 2 2 2; 0 2 0"),
        np.matrix("0 0 3; 0 0 3; 3 3 3"),
        np.matrix("4; 4; 4; 4"),
        np.matrix("5 5; 5 5"),
    ]

    jet_patterns: str
    jet_pattern_index: int = 0

    def __init__(self, input_: str):
        self.jet_pattern_index = 0
        self.space = np.zeros((0, self.WIDTH), dtype=int)
        self.jet_patterns = input_

    def get_jet_pattern(self):
        result = self.jet_patterns[self.jet_pattern_index]
        self.jet_pattern_index = (self.jet_pattern_index + 1) % len(self.jet_patterns)
        return result

    def extend_cave_for(self, rock: NDArray):
        new_height = self.get_height() + 1 + rock.shape[0] + 3
        diff = new_height - self.space.shape[0]
        if diff == 0:
            return
        if diff < 0:
            self.space = self.space[abs(diff):]
        else:
            self.space = np.vstack([np.zeros((diff, 7), dtype=int), self.space])

    def insert_rock(self, rock: NDArray):
        pos = self.get_entrance_pos(rock)
        if not self.can_fit_rock(rock, pos):
            raise Exception(f"Could not insert rock {rock}")
        while True:
            if DEBUG_LEVEL > 1:
                self.print_with_rock(rock, pos)

            pos = pos.apply(self.get_jet_pattern())
            if not self.can_fit_rock(rock, pos):
                pos = pos.revert()
            pos = pos.lower()
            if not self.can_fit_rock(rock, pos):
                break
        pos = pos.revert()
        self.place_rock(rock, pos)
        if DEBUG_LEVEL > 0:
            print(self)

    def insert_rocks(self, amount: int):
        for i in range(amount):
            rock_index = i % len(self.rocks)
            rock = self.rocks[rock_index]
            self.extend_cave_for(rock)
            self.insert_rock(rock)

    def get_top_row(self):
        return max(np.argwhere(~self.space.any(axis=1)), default=[0])[0]

    def get_height(self):
        top_row = self.get_top_row()
        height = self.space.shape[0] - top_row -1
        return height

    def get_entrance_pos(self, rock: NDArray):
        height, width = rock.shape
        left = 2
        right = left + width

        bottom = self.get_top_row() - 2
        top = bottom - height

        return Position(left=left, right=right, bottom=bottom, top=top)

    def can_fit_rock(self, rock: NDArray, pos: Position):
        if pos.bottom > self.space.shape[0]:
            return False
        result = not np.any(self.space[pos.top:pos.bottom, pos.left:pos.right].astype(bool) & rock.astype(bool))
        return result

    def place_rock(self, rock: NDArray, pos: Position):
        self.space[pos.top:pos.bottom, pos.left:pos.right] = self.space[pos.top:pos.bottom, pos.left:pos.right] | rock

    def print_with_rock(self, rock: NDArray, pos: Position):
        temp_rock = rock.copy()
        temp_rock[temp_rock == 1] = 2
        temp_cave = deepcopy(self)
        temp_cave.place_rock(temp_rock, pos)
        print(temp_cave)

    def __str__(self):
        mat = self.space.copy().astype(str)
        mat[mat == '0'] = '.'
        # mat[mat == '1'] = '#'
        # mat[mat == '2'] = '@'
        res = ''
        for r in mat:
            res += f'|{"".join(r)}|\n'
        res += f'+{"-" * 7}+\n'
        return res


class Puzzle17(PuzzleToSolve):
    @property
    def day(self) -> int:
        return 17

    @property
    def test_input(self) -> str:
        return ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"

    @property
    def test_answer_a(self):
        return 3068

    @property
    def test_answer_b(self):
        return 1514285714288

    def a(self, input_: str):
        chamber = Chamber(input_)
        chamber.insert_rocks(2022)
        print(chamber)
        result = chamber.get_height()
        return result

    def b(self, input_: str):
        chamber = Chamber(input_)
        chamber.insert_rocks(1000000000000)
        print(chamber)
        result = chamber.get_height()
        return result

DEBUG_LEVEL=0
puzzle = Puzzle17()
puzzle.solve()
