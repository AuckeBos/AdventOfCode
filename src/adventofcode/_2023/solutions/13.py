from typing import List
from adventofcode._templates.v20231204.puzzle_to_solve import PuzzleToSolve
from adventofcode.helpers.base_matrix import BaseMatrix
import numpy as np

class Pattern(BaseMatrix):
    """
    A patern of ash and rocks. 
    Can search the mirror and return the score.
    Can also find the smudge, clean it, and return the score.
    """
    
    mirror_index: int = None
    mirror_is_row: bool = None
    
    def clean_and_search_mirror(self):
        """
        First find the mirror. Then try for each position:
        - Flip it (clean the possible smudge)
        - Check whether we can find the mirror for the cleaned pattern
        - If found, this is the smudge location, and we can return the score
        - If not found, continue
        """
        self.find_mirror()
        for r, c in self.iter_topleft_to_bottomright():
            original_value = self.data[r, c]
            new_value = "#" if original_value == "." else "."
            self.data[r, c] = new_value
            if score := self.compute_score():
                return score
            self.data[r, c] = original_value
        raise Exception("No smudge found")

    def compute_score(self):
        """
        First find the mirror. If it's found, return the score
        """
        if not self.find_mirror():
            return None
        if self.mirror_is_row:
            return 100 * (self.mirror_index + 1)
        else:
            return self.mirror_index + 1
    
    def search_mirror(self, is_row: bool) -> bool:
        """
        Search the mirror. The mirror is at the position where the pattern is the same on both sides.
        
        :param is_row: Whether to search the mirror in the rows or columns.
        :return: Whether the mirror was found.
        """
        # Iterating over rows or columns
        shape_index = 0 if is_row else 1
        # Loop over the rows/columns
        for i in range(0, self.data.shape[shape_index] - 1):
            # If the smudged pattern already had the mirror here, it can't be the position for the cleaned mirror
            if (is_row and self.mirror_is_row and i == self.mirror_index) or (not is_row and not self.mirror_is_row and i == self.mirror_index):
                continue
            x1_i, x2_i = i, i + 1
            # While the pattern is the same on both sides, keep going
            while x1_i >= 0 and x2_i < self.data.shape[shape_index]:
                # Load either row or col
                r_1 = self.data[x1_i] if is_row else self.data[:, x1_i]
                r_2 = self.data[x2_i] if is_row else self.data[:, x2_i]
                # If not equal, this is not the mirror position, hence stop
                if not np.all(r_1 == r_2):
                    break
                # Both rows/cols equal. Go one step further
                x1_i -= 1
                x2_i += 1
            else:
                # All rows/cols equal. We found the mirror
                self.mirror_index = i
                self.mirror_is_row = is_row
                return True
        return False
    
    def find_mirror(self) -> bool:
        """
        Search the mirror in both rows and columns. Return whether the mirror was found.
        """
        return self.search_mirror(is_row=True) or self.search_mirror(is_row=False)
    
    def __repr__(self):
        str_ = ""
        for r in range(self.data.shape[0]):
            for c in range(self.data.shape[1]):
                str_ += self.data[r, c]
            str_ += "\n"
        return str_    
        

class Puzzle13(PuzzleToSolve):
    @property
    def day(self) -> int:
        return 13
    
    @property
    def year(self) -> int:
        return 2023

    @property
    def test_input(self) -> str:
        return """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#"""

    @property
    def test_answer_a(self):
        return 405

    @property
    def test_answer_b(self):
        return 400

    def parse_input(self, input_: str) -> List[Pattern]:
        patterns = []
        pattern_strs = input_.split("\n\n")
        for pattern_str in pattern_strs:
            pattern = Pattern()
            pattern.parse_input(pattern_str, pad=None)
            patterns.append(pattern)
        return patterns
            

    def a(self, patterns: List[Pattern]) -> int:
        """
        Return the sum of the scores of the patterns
        """
        return sum(pattern.compute_score() for pattern in patterns)

    def b(self, patterns: List[Pattern]) -> int:
        """
        Return the sum of the scores of the patterns, after cleaning the smudge
        """
        return sum(pattern.clean_and_search_mirror() for pattern in patterns)


puzzle = Puzzle13()
puzzle.solve()
