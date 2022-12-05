from numpy.typing import NDArray

from puzzle_to_solve import PuzzleToSolve
import numpy as np
import string
import re
import pandas as pd


class Board:
    matrix: NDArray
    movements: []
    alphabet = string.ascii_uppercase

    def set_matrix(self, input: str):
        self.matrix = np.empty((100, 100))
        self.matrix[:] = np.NaN
        input = input.replace("   ", "[0]").replace("][", "] [")
        # Split and drop number row
        rows = input.split("\n")[:-1]
        rows.reverse()
        for i, row in enumerate(rows):
            cells = row.split(" ")
            for j, cell in enumerate(cells):
                stripped = cell.strip()
                if not stripped:
                    continue
                letter = stripped[1]
                if letter == '0':
                    continue
                number = self.letter_to_int(letter)
                self.matrix[100 - i - 1, j] = number
        return self

    def set_movements(self, input: str):
        movements = []
        rows = input.split("\n")
        for row in rows:
            if not row.strip():
                continue
            values = re.search("move (\d) from (\d) to (\d)", row).groups()
            values = [int(v) for v in values]
            movements.append(values)
        self.movements = movements



    def letter_to_int(self, letter: str):
        if letter not in self.alphabet:
            raise Exception(f'Cell {letter} is invalid')
        return self.alphabet.index(letter)
    def int_to_letter(self, value):
        return self.alphabet[value]

    def apply_movements(self):
        for (amount, source, dest) in self.movements:
            frame = pd.DataFrame(self.matrix)
            j = source - 1
            i_start = frame.loc[:, j].first_valid_index()
            i_end = i_start + amount
            values = self.matrix[i_start:i_end, j].copy()
            self.matrix[i_start:i_end, j] = np.NaN

            j = dest - 1
            try:
                i_start = frame.loc[:, j].first_valid_index() - amount
            except:
                i_start = 100 - amount
            i_end = i_start + amount
            self.matrix[i_start:i_end, j] = values
            print(self.matrix)


class Puzzle5(PuzzleToSolve):
    @property
    def day(cls) -> int:
        return 5

    @property
    def test_input(self) -> str:
        return """    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
        """

    @property
    def test_answer_a(self):
        return 'CMZ'

    @property
    def test_answer_b(self):
        return 12

    def parse_input(self, input: str) -> Board:
        board_str, movements_str = input.split("\n\n")
        board = Board()
        board.set_matrix(board_str)
        board.set_movements(movements_str)
        return board

    def a(self, input: str):
        board = self.parse_input(input)
        board.apply_movements()
        frame = pd.DataFrame(board.matrix)
        result = ''
        for col in frame.columns:
            i = frame.loc[:, col].first_valid_index()
            if not i:
                continue
            number = int(frame.loc[i, col])
            letter = board.int_to_letter(number)
            result += letter
        return result




    def b(self, input: str):
        return None


puzzle = Puzzle5()
puzzle.solve()
