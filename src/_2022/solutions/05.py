from numpy.typing import NDArray

from src._2022.puzzle_to_solve import PuzzleToSolve
import numpy as np
import string
import re
import pandas as pd


class Board:
    """
    A Board can parse input, apply movements, and compute the result.
    Attributes
    ---------
    frame: pd.DataFrame
        Contains the parsed input. Letters are converted to int, based on their alphabet index. Has size 100x100,
        to make sure columns can be stacked without index-overflow.
    movements: List[Tuple(int, int, int)]
        Will contain a list of movements, as triples: amount, from, to
    mover_type: int
        Either 9000 or 9001. Mover type defines whether a full stack is moved at once, or crate-by-crate
    MATRIX_SIZE: int
        Static size of the frame. Must be large enough to hold the input data

    """
    frame: pd.DataFrame
    movements: []
    mover_type: int
    alphabet = string.ascii_uppercase
    MATRIX_SIZE = 100

    def __init__(self, input: str, mover_type: int):
        """
        Initialize a board:
        - Set the mover type
        - Create the frame with values
        - Load the movement list
        - Set the mover type
        """
        if not mover_type in [9000, 9001]:
            raise Exception(f'There is no CrateMover {mover_type}')
        board_str, movements_str = input.split("\n\n")
        self.set_matrix(board_str)
        self.set_movements(movements_str)
        self.mover_type = mover_type

    def set_matrix(self, input: str):
        """
        Based the string representation of the board, create a pandas frame:
        - Create self.matrix_sizexself.matrix_size NaN matrix, to be filled
        - Replace '   ' with [0], for each iteration of rows
        - Loop over the rows in reverse (we start at the bottom left of the matrix)
        - Split the cells of the rows using " "
        - Loop over the cells. If the [0] cell is found, skip it
        - Else: convert letter to int, and set it in the matrix (at the bottom instead of top)
        - Set self.frame as the pd frame of the matrix. Easier because it has a method first_valid_index
        """
        matrix = np.empty((self.MATRIX_SIZE, self.MATRIX_SIZE))
        matrix[:] = np.NaN
        input = input.replace("    ", "[0]").replace("][", "] [")
        # Split and drop number row
        rows = input.split("\n")[:-1]
        rows.reverse()
        for i, row in enumerate(rows):
            cells = row.split(" ")
            for j, cell in enumerate(cells):
                letter = cell.strip()[1]
                if letter == '0':
                    continue
                number = self.letter_to_int(letter)
                matrix[self.MATRIX_SIZE - i - 1, j] = number
        self.frame = pd.DataFrame(matrix)
        return self

    def set_movements(self, input: str):
        """
        Parse the list of movements, into triples amount,from,to. Set as self.movements
        """
        movements = []
        rows = input.split("\n")
        for row in rows:
            if not row.strip():
                continue
            values = re.search("move (\d+) from (\d+) to (\d+)", row).groups()
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
        """
        Apply self.movements on self.frame:
        - Get the top 'amount' indexes of 'source' Use first_valid_index to find row counts
        - If the self.mover_type is 9000 (puzzle a), we flip the values: The CraneMover moves
            one-by-one, hence it reverts. Else (9001: b)), do not revert: it moves the whole stack at once
        - Get the destination. Use first_valid_index - amount to make sure we place it on top of the existing values
        - Set values in destination
        """
        for (amount, source, dest) in self.movements:
            # Get source, and the set source to NaN
            j = source - 1
            i_start = self.frame.iloc[:, j].first_valid_index()
            i_end = i_start + amount
            values = self.frame.iloc[i_start:i_end, j].copy()
            if self.mover_type == 9000:
                values = np.flip(values)

            self.frame.iloc[i_start:i_end, j] = np.NaN

            # Get destination, set values
            j = dest - 1
            i_start = self.frame.iloc[:, j].first_valid_index()
            # If not i_start, we have a empty column. Hence bottom - amount
            if not i_start:
                i_start = self.MATRIX_SIZE - amount
            else:  # Else we found the top of the column, decrease with amount to put the stack on top
                i_start = i_start - amount
            i_end = i_start + amount
            self.frame.iloc[i_start:i_end, j] = values

    def compute_result(self):
        """
        After movements have been applied, get a string with the top-letter of each column
        """
        result = ''
        for col in self.frame.columns:
            i = self.frame.iloc[:, col].first_valid_index()
            if not i:
                continue
            number = int(self.frame.iloc[i, col])
            letter = self.int_to_letter(number)
            result += letter
        return result


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
        return 'MCD'

    def a(self, input_: str):
        """
        Solve a), by creating a board with CrateMover 9000, applying movements, and return the result
        """
        board = Board(input_, 9000)
        board.apply_movements()
        return board.compute_result()

    def b(self, input_: str):
        """
        Solve b), by creating a board with CrateMover 9001, applying movements, and return the result
        """
        board = Board(input_, 9001)
        board.apply_movements()
        return board.compute_result()


puzzle = Puzzle5()
puzzle.solve()
