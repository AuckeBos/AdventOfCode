from typing import Tuple, List

from numpy import ndarray
from adventofcode._templates.v20231204.puzzle_to_solve import PuzzleToSolve
from adventofcode.helpers.base_matrix import BaseMatrix
import numpy as np
import sys
import copy

class Contraption(BaseMatrix):
    energy: ndarray
    visited: List[Tuple[Tuple[int, int], Tuple[int, int]]]
    
    def parse_input(self, input_: str, pad: str = "."):
        super().parse_input(input_, pad)
        self.reset()
    
    def reset(self):
        self.energy = np.full(self.data.shape, '.')
        self.visited = []
        
    def new_beams(self, position: Tuple[int, int], direction: Tuple[int, int], type_: str) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """
        Find the new beams, given the current position, direction and type
        
        Args:
            position: current position
            direction: current direction
            type_: current type
            
        Returns:
            List of new beams, as tuples of (position, direction)
        """
        if type_ == ".": # Don't change direction
            directions = [direction]
        elif type_ == "|": # If moving vertical, stay vertical, else split into vertical
            directions = [direction] if direction in [(1, 0), (-1, 0)] else [(1, 0), (-1, 0)]
        elif type_ == "-": # If moving horizontal, stay horizontal, else split into horizontal
            directions = [direction] if direction in [(0, 1), (0, -1)] else [(0, 1), (0, -1)]
        elif type_ == "/": # Process the mirror
            directions = [(-direction[1], -direction[0])]
        elif type_ == "\\": # Process the mirror
            directions = [(direction[1], direction[0])]        
        else:
            raise ValueError(f"Invalid type: {type_}")
        return [((position[0] + d[0], position[1] + d[1]), d) for d in directions]
    
    
    def process_beam(self, r: int, c: int, direction: Tuple[int, int]) -> int:
        """
        Process a beam, given the starting position and direction.
        do a BFS, and return the number of visited fields.
        Visited is a list of tuples of (position, direction). This is to prevent going back and forth.
        """
        visited = []
        to_process = [((r, c), direction)]
        while len(to_process) > 0:
            (r, c), direction = to_process.pop()
            type_ = self.data[r, c]
            if ((r, c), direction) in visited or type_ == "#":
                continue
            visited.append(((r, c), direction))
            to_process.extend(self.new_beams((r, c), direction, type_))
        return len(set([(r, c) for (r, c), _ in visited]))


class Puzzle16(PuzzleToSolve):
    @property
    def day(self) -> int:
        return 16
    
    @property
    def year(self) -> int:
        return 2023

    @property
    def test_input(self) -> str:
        return """.|...\\....
|.-.\\.....
.....|-...
........|.
..........
.........\\
..../.\\\..
.-.-/..|..
.|....-|.\\
..//.|...."""

    @property
    def test_answer_a(self):
        return 46

    @property
    def test_answer_b(self):
        return 51

    def parse_input(self, input_: str) -> Contraption:
        """
        A contraption is a matrix of characters. The # denotes a wall.
        """
        contraption = Contraption()
        contraption.parse_input(input_, "#")
        return contraption
    
    def find_max_energy(self, contraption: Contraption, starting_points: List[Tuple[int, int, Tuple[int, int]]]) -> int:
        """
        Find the max energy, given a list of starting points.
        """
        result = 0
        for i, starting_point in enumerate(starting_points):
            print(f"Processing {i} of {len(starting_points)}")
            result = max(result, contraption.process_beam(*starting_point))
            contraption.reset()
        return result

    def a(self, contraption: Contraption):
        """
        Find the energy of the contraption, given the starting point (1, 1) and direction (0, 1)
        """
        return self.find_max_energy(contraption, [(1, 1, (0, 1))])
    
    def get_entrypoints(self, contraption: Contraption) -> List[Tuple[int, int, Tuple[int, int]]]:
        """
        Get the entrypoints of the contraption. These are the outer edges. Exclude padding. Used in b)
        """
        r_range = range(1, contraption.data.shape[0] - 1)
        c_range = range(1, contraption.data.shape[1] - 1)
        return [(r, 1, (0, 1)) for r in r_range] + [(r, contraption.data.shape[1] - 2, (0, -1)) for r in r_range] + [(1, c, (1, 0)) for c in c_range] + [(contraption.data.shape[0] - 2, c, (-1, 0)) for c in c_range]        

    def b(self, contraption: Contraption):
        """
        Find the max energy, given the entrypoints of the contraption.
        """
        starting_points = self.get_entrypoints(contraption)
        return self.find_max_energy(contraption, starting_points)


puzzle = Puzzle16()
puzzle.solve()
