from itertools import combinations
from string import ascii_lowercase, ascii_uppercase, digits

import numpy as np

from adventofcode._templates.v20231204.puzzle_to_solve import PuzzleToSolve
from adventofcode.helpers.base_matrix import BaseMatrix, Position


class City(BaseMatrix):
    FREQUENCIES: list[str] = [*ascii_lowercase, *ascii_uppercase, *digits]

    def find_antinodes(self, *, apply_resonant_harmonics: bool) -> list[str]:
        """
        Find all antinodes in the city.

        Loop over all pairs of frequencies. Add all antinodes of the pair.
        apply_resonant_harmonics = False for a, apply_resonant_harmonics = True for b
        """
        return set(  # Deduplicate
            location
            for frequency in self.FREQUENCIES  # Loop over all frequencies types
            for (a, b) in combinations(  # Loop over all pairs
                np.argwhere(self.data == frequency), 2
            )
            for location in self.antinode_locations(  # Find all antinode locations of the pair
                Position(*a),
                Position(*b),
                apply_resonant_harmonics=apply_resonant_harmonics,
            )
        )

    def antinode_locations(
        self, a: Position, b: Position, *, apply_resonant_harmonics: bool
    ) -> list[Position]:
        """Get all antinode locations for a pair of equal frequencies."""
        if not apply_resonant_harmonics:
            # Only distance of 1
            result = [
                location
                for location in [(a + a - b), (b + b - a)]
                if self.is_in_bounds(location)
            ]
        else:
            # All distances, as long as they are in bounds
            result = set()
            for left, right in [(a, b), (b, a)]:
                location = left
                while self.is_in_bounds(location):
                    result.add(location)
                    location += left - right
        return result


class Puzzle8(PuzzleToSolve):
    @property
    def day(self) -> int:
        return 8

    @property
    def year(self) -> int:
        return 2024

    @property
    def test_input(self) -> str:
        return """............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............"""

    @property
    def test_answer_a(self):
        return 14

    @property
    def test_answer_b(self):
        return 34

    def parse_input(self, input_: str) -> City:
        return City(input_, pad=None, dtype=str)

    def a(self, city: City):
        return len(city.find_antinodes(apply_resonant_harmonics=False))

    def b(self, city: City):
        return len(city.find_antinodes(apply_resonant_harmonics=True))


puzzle = Puzzle8()
puzzle.solve()
