import numpy as np

from adventofcode._templates.v20231204.puzzle_to_solve import PuzzleToSolve
from adventofcode.helpers.base_matrix import BaseMatrix


class WordSearch(BaseMatrix):
    mask: np.ndarray

    def search_word(self, i: int, j: int, word: str, adjacent_fields: list) -> bool:
        if self.data[i, j] != word[0]:
            return 0
        if len(word) == 1:
            return 1
        return sum(
            self.search_word(
                adjacent_i,
                adjacent_j,
                word[1:],
                [(adjacent_i + (adjacent_i - i), adjacent_j + (adjacent_j - j))],
            )
            for adjacent_i, adjacent_j in adjacent_fields
        )

    def solve_a(self) -> int:
        return sum(
            self.search_word(i, j, "XMAS", self.adjacent_fields(i, j))
            for i, j in self.iter_topleft_to_bottomright()
        )

    def solve_b(self) -> int:
        pass


class Puzzle4(PuzzleToSolve):
    @property
    def day(self) -> int:
        return 4

    @property
    def year(self) -> int:
        return 2024

    @property
    def test_input(self) -> str:
        return """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""

    @property
    def test_answer_a(self):
        return 18

    @property
    def test_answer_b(self):
        return None

    def parse_input(self, input_: str) -> WordSearch:
        word_search = WordSearch()
        word_search.parse_input(input_)
        return word_search

    def a(self, word_search: WordSearch):
        return word_search.solve_a()

    def b(self, input_: str):
        return -1


puzzle = Puzzle4()
puzzle.solve()
