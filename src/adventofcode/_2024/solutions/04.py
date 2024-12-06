import numpy as np

from adventofcode._templates.v20231204.puzzle_to_solve import PuzzleToSolve
from adventofcode.helpers.base_matrix_v1 import BaseMatrixV1


class WordSearch(BaseMatrixV1):
    mask: np.ndarray

    def search_word(
        self, i: int, j: int, word: str, adjacent_fields: list
    ) -> list[tuple[int, int]]:
        """
        Find all directions in which the word is found, starting at i, j
        Only take the adjacent_fields into account.
        Return a list of all directions in which the word is found
        """
        # Word not found
        if self.data[i, j] != word[0]:
            return []
        # Word found, but direction unknown. Return singleton. Parent will convert to direction
        if len(word) == 1:
            return [()]
        return [
            # Return each direction in which the word is found
            self.direction((i, j), (adjacent_i, adjacent_j))
            for adjacent_i, adjacent_j in adjacent_fields
            # Only return it if the adjacent is the last letter of the word
            if len(
                self.search_word(
                    adjacent_i,
                    adjacent_j,
                    word[1:],
                    [
                        self.add(
                            (adjacent_i, adjacent_j),
                            self.direction((i, j), (adjacent_i, adjacent_j)),
                        )
                    ],
                )
            )
            == 1
        ]

    def solve_a(self) -> int:
        """
        Count all the XMAS in the matrix
        """
        return sum(
            len(self.search_word(i, j, "XMAS", self.adjacent_fields(i, j)))
            for i, j in self.iter_topleft_to_bottomright()
        )

    def solve_b(self) -> int:
        """
        Find all X-MASes (crossing MASes).

        - Loop over all cells in the matrix
        - If the cell is the start of a diagonal MAS:
            - Check if the two corners (in the direction of the MAS) are either M and S or S and M
            - If so, count 1
        - We have counted each leg of the X-MASes. So divide by 2, since we need to count X-MASes
        """
        return (
            sum(
                [
                    1  # We have a MAS, and a crossing MAS: X-MAS
                    if "".join(
                        [
                            self.data[i, j + 2 * direction[1]],
                            self.data[i + 2 * direction[0], j],
                        ]
                    )  # The two corners are either M and S or S and M
                    in [
                        "MS",
                        "SM",
                    ]
                    else 0  # We have a MAS, but no X-MAS
                    for i, j in self.iter_topleft_to_bottomright()  # Loop over all cells
                    for direction in self.search_word(  # Find the directions in which a MAS is found
                        i,
                        j,
                        "MAS",
                        self.adjacent_fields(i, j, horizontal_vertical=False),
                    )
                ]
            )
            // 2
        )


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
        return 9

    def parse_input(self, input_: str) -> WordSearch:
        word_search = WordSearch()
        word_search.parse_input(input_)
        return word_search

    def a(self, word_search: WordSearch):
        return word_search.solve_a()

    def b(self, word_search: WordSearch):
        return word_search.solve_b()


puzzle = Puzzle4()
puzzle.solve()
