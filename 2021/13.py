from itertools import combinations, permutations, product
from typing import List, Set, Dict, Optional, Tuple

import numpy as np
from aocd.models import Puzzle
from numpy.typing import NDArray


class Map:
    map: NDArray
    def __init__(self, points: List[str]):
        points_split = np.array([np.array(p.split(','), dtype=int) for p in points])
        max_c, max_r = max(points_split[:,0]) + 1,max(points_split[:,1]) + 1
        self.map = np.full((max_r, max_c), fill_value=False, dtype=bool)
        for p in points_split:
            self.map[p[1], p[0]] = True

    def fold(self, lines: List[str]):
        for line in lines:
            axis, value = self.parse_fold_line(line)
            self._fold(axis, value)

    def _fold(self, axis: int, value: int):
        l, r = np.array_split(self.map, [value], axis=axis)
        r = np.delete(r, (0), axis=axis)
        r = np.flip(r, axis)
        self.map = np.logical_or(l, r)


    def parse_fold_line(self, line: str) -> Tuple[int, int]:
        l, r = line.split('=')
        axis = int(l[-1] == 'x')
        value = int(r)
        return axis, value





puzzle = Puzzle(year=2021, day=13)
points, folds = puzzle.input_data.split("\n\n")
map = Map(points.splitlines())
map.fold([folds.splitlines()[0]])
puzzle.answer_a = np.count_nonzero(map.map)

map = Map(points.splitlines())
map.fold(folds.splitlines())
print('The answer to part 2 is:')
map_str = map.map.astype(str)
map_str[map_str == 'True'] = '█'
map_str[map_str == 'False'] = ' '
for r in map_str:
    print(''.join([x for x in r]))