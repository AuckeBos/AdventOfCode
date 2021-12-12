from itertools import combinations, permutations, product
from typing import List, Set, Dict, Optional

import numpy as np
from aocd.models import Puzzle
from numpy.typing import NDArray


class Cave:
    neighbours: Set["Cave"]
    name: str
    n_visited: int

    def __init__(self, name: str):
        self.name = name
        self.neighbours = set()
        self.n_visited = 0

    @property
    def is_large(self):
        return self.name.isupper()

    def can_vist(self, allow_double: bool):
        if self.is_large:
            return True
        if (not allow_double) or self.is_start or self.is_end:
            return self.n_visited == 0
        # Allow double, self is small
        return not self.is_doubly_visit

    @property
    def is_end(self):
        return self.name == "end"

    @property
    def is_start(self):
        return self.name == "start"

    @property
    def is_doubly_visit(self):
        return self.n_visited > 1

    def visit(self):
        self.n_visited += 1

    def unvisit(self):
        self.n_visited -= 1

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return self.name

    def add_neighbour(self, c: "Cave"):
        self.neighbours.add(c)


class Map:
    caves: Dict[str, Cave]
    visited: List[Cave]

    # Counter for num valid paths found
    n_paths_found: int

    # True for pt 2. Allow one small cave to be visited twice (not start,end)
    allow_one_double_visit: bool
    # True if we have visited one small cave twice in the current path
    visited_double_once: bool

    def __init__(self, lines: List[str], allow_one_double_visit: bool):
        self.allow_one_double_visit = allow_one_double_visit
        self.visited_double_once = False
        self.caves = {}
        for line in lines:
            self.split_line(line)

    def split_line(self, line: str):
        l, r = line.split("-")
        if l not in self.caves:
            self.caves[l] = Cave(l)
        if r not in self.caves:
            self.caves[r] = Cave(r)
        self.caves[l].add_neighbour(self.caves[r])
        self.caves[r].add_neighbour(self.caves[l])

    def count_paths(self):
        self.n_paths_found = 0
        self.visited = []
        start = [cave for cave in self.caves.values() if cave.is_start][0]
        self.search(start)
        return self.n_paths_found

    def save_visited(self):
        self.n_paths_found += 1
        self.unvisit(self.visited[-1])

    def visit(self, cave: Cave):
        cave.visit()
        # If this cave is now doubly visited, disallow double visits from now on
        self.visited_double_once |= (cave.is_doubly_visit and not cave.is_large)
        self.visited.append(cave)

    def unvisit(self, cave: Cave):
        # If this was the cave we visited twice, now re-allow double visits
        self.visited_double_once &= not (cave.is_doubly_visit and not cave.is_large)
        cave.unvisit()
        # Remove from current path
        self.visited = self.visited[:-1]

    def search(self, cave: Cave):
        if not cave.can_vist(
            self.allow_one_double_visit and not self.visited_double_once
        ):
            return
        self.visit(cave)
        if cave.is_end:
            self.save_visited()
            return
        for n in cave.neighbours:
            self.search(n)
        self.unvisit(cave)


puzzle = Puzzle(year=2021, day=12)
lines = puzzle.input_data.splitlines()
puzzle.answer_a = Map(lines, False).count_paths()
puzzle.answer_b = Map(lines, True).count_paths()
