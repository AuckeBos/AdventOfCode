import numpy as np

from adventofcode._templates.v20231204.puzzle_to_solve import PuzzleToSolve
from adventofcode.helpers.base_matrix import BaseMatrix, Directions, Position


class Garden(BaseMatrix):
    def __init__(self, input_: str):
        super().__init__(input_, pad=None, dtype=str)
        self.groups = np.full(self.data.shape, 0, dtype=int)
        self.fences = np.full(self.data.shape, 0, dtype=int)
        self.sides = np.full(self.data.shape, None, dtype=list)
        self.sidecounts = np.full(self.data.shape, 0, dtype=int)

    def is_handled(self, p: Position):
        return self.groups[p.tuple_] != 0

    def count_fences(self, p: Position):
        fences = 0
        neighbors = [
            p + d
            for d in Position.directions(include_axis=True, include_diagonal=False)
        ]
        for n in neighbors:
            if (not self.is_in_bounds(n)) or self[p] != self[n]:
                fences += 1
        return fences

    def find_sides(self, pos: Position) -> list:
        if pos.i == 3 and pos.j == 3:
            # should be 3, but is 2. top is counted, right is not counted (ok). left is not counted (nok). Becuase one space more to the right is already counted
            # test = np.full(self.sidecounts.shape, '.', dtype=str)
            # test[np.where(self.data == "C")] = self.sidecounts[self.data == "C"]
            # print(self.matrix_to_str(test))            
            test = ""        
        if pos.i == 3 and pos.j == 4:
            test = ""
            
        sides_handled = set()
        sides_counted = 0
        directions = Directions.ALL.value
        for i, direction in enumerate(directions):
            if (
                self.is_in_bounds(pos + direction)
                and self[pos + direction] == self[pos]
            ):
                continue
            perpendicular_directions = [
                directions[(i - 1) % len(directions)],
                directions[(i + 1) % len(directions)],
            ]
            for perpendicular_direction in perpendicular_directions:
                i = 1
                yet_handled = False
                while True:
                    new_pos = pos + perpendicular_direction * i
                    if (not self.is_in_bounds(new_pos)) or self[new_pos] != self[pos] or (
                        self.is_handled(new_pos) and direction not in self.sides[new_pos.tuple_]
                    ):
                        break
                    if self.is_in_bounds(new_pos + direction) and self[new_pos + direction] == self[pos]:
                        break                
                    # This statemented fixes C but breaks V
                    # if not self.is_handled(new_pos):
                        # break
                    if (
                        self.is_handled(new_pos)
                        and direction in self.sides[new_pos.tuple_]
                    ):
                        yet_handled = True
                        break
                    i += 1
                if yet_handled:
                    break

            if not yet_handled:
                sides_counted += 1
            sides_handled.add(direction)
        self.sidecounts[pos.tuple_] = sides_counted
        self.sides[pos.tuple_] = list(sides_handled)

    def handle(self, p: Position):
        if self.is_handled(p):
            return
        self.fences[p.tuple_] = self.count_fences(p)
        self.find_sides(p)
        neighbors = self.adjacent_fields(p)
        for n in neighbors:
            if self[p] == self[n] and self.groups[n.tuple_] != 0:
                group = self.groups[n.tuple_]
                break
        else:
            group = np.max(self.groups) + 1
            print(f"Found new group for {p.tuple_}: {self[p]}")
        self.groups[p.tuple_] = group
        for n in neighbors:
            if self[p] == self[n]:
                self.handle(n)

    def flood(self):
        for p in list(self.iter_topleft_to_bottomright())[::-1]:
            if self.is_handled(p):
                continue
            self.handle(p)


class Puzzle12(PuzzleToSolve):
    @property
    def day(self) -> int:
        return 12

    @property
    def year(self) -> int:
        return 2024

    @property
    def test_input(self) -> str:
        return """RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE"""

    @property
    def test_answer_a(self):
        return 1930

    @property
    def test_answer_b(self):
        return 1206

    def parse_input(self, input_: str) -> Garden:
        return Garden(input_)

    def a(self, garden: Garden):
        garden.flood()
        result = 0
        for group in range(1, np.max(garden.groups) + 1):
            fences = np.sum(garden.fences[garden.groups == group])
            size = np.sum(garden.groups == group)
            letter = garden.data[garden.groups == group][0][0][0]
            print(f"Group {group} ({letter}): {size} * {fences} = {size * fences}")
            result += size * fences
        return result

    def b(self, garden: Garden):
        garden.flood()
        result = 0
        for group in range(1, np.max(garden.groups) + 1):
            sides = np.sum(garden.sidecounts[garden.groups == group])
            size = np.sum(garden.groups == group)
            letter = garden.data[garden.groups == group][0][0][0]
            # print(f"Group {group} ({letter}): {size} * {sides} = {size * sides}")
            
            test = np.full(garden.sidecounts.shape, '.', dtype=str)
            test[np.where(garden.groups == group)] = garden.sidecounts[garden.groups == group]
            # print(garden.matrix_to_str(test))

            result += size * sides
        # print(garden.matrix_to_str(garden.sidecounts))
        return result


puzzle = Puzzle12()
# puzzle.solve_exercise("b")
puzzle.solve()
