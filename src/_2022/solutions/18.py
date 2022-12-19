from typing import List

import numpy as np

from src._2022.puzzle_to_solve import PuzzleToSolve


class Puzzle18(PuzzleToSolve):
    RELATIVE_NEIGHBOURS = [
        (0, 0, -1),
        (0, 0, 1),
        (0, 1, 0),
        (0, -1, 0),
        (1, 0, 0),
        (-1, 0, 0),
    ]

    cubes: List[str]

    @property
    def day(self) -> int:
        return 18

    @property
    def test_input(self) -> str:
        return """2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5"""

    @property
    def test_answer_a(self):
        return 64

    @property
    def test_answer_b(self):
        return 58

    def get_neighbours(self, cube: str):
        result = []
        pos = np.array([int(i) for i in cube.split(',')])
        for rel_n in self.RELATIVE_NEIGHBOURS:
            n = pos + rel_n
            n_str = ','.join(map(str, n))
            result.append(n_str)
        return result

    def count_free_sides(self, cube: str):
        result = 0
        for n in self.get_neighbours(cube):
            if n not in self.cubes:
                result += 1
        return result



    def a(self, input_: str):
        self.cubes = input_.splitlines()
        result = sum([self.count_free_sides(cube) for cube in self.cubes])
        return result

    def b(self, input_: str):
        self.cubes = input_.splitlines()
        total_free_sides = sum([self.count_free_sides(cube) for cube in self.cubes])
        unreachable_cubes = [cube for cube in self.cubes if self.count_free_sides(cube) <= 1]
        unreachable_sides = []
        for c in unreachable_cubes:
            unreachable_sides.extend(self.get_neighbours(c))
        n_unreachable_sides = len(set(unreachable_sides))
        result = total_free_sides - n_unreachable_sides
        return result

puzzle = Puzzle18()
puzzle.solve()
