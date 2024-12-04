from typing import List, Tuple, Union

import numpy as np


class BaseMatrix:
    """
    Matrix class, to be used as a base class for other matrix classes
    Parses input into a numpy matrix, and provides some helper functions

    Attributes:
        data: the numpy matrix
        pad: the padding used to surround the matrix
    """

    data: np.ndarray
    pad: str

    def parse_input(self, input_: str, pad: str = "."):
        """
        Input string to numpy matrix. Surround matrix with pad, to make sure we don't get index errors

        Args:
            input_: input string
            pad: padding to add to the matrix. If None, no padding is added
        """
        self.pad = pad
        # Create numpy character matrix from input
        self.data = np.array([list(line) for line in input_.split("\n")])
        if pad is not None:
            # Surround matrix with ".", to make sure we don't get index errors
            self.data = np.pad(self.data, 1, constant_values=pad)

    def iter_topleft_to_bottomright(self):
        """
        Yield all indices from top left to bottom right. Do not iterate of the pad
        """
        start_at = 1 if self.pad is not None else 0
        for i in range(start_at, self.data.shape[0] - (start_at)):
            for j in range(start_at, self.data.shape[1] - (start_at)):
                yield i, j

    def fields_to_values(self, fields: List[Tuple[int, int]]):
        """
        Get the values of a list of fields
        """
        return [self.data[i, j] for i, j in fields]

    def adjacent_fields(
        self,
        i: int,
        j: int,
        *,
        as_values: bool = False,
        horizontal_vertical: bool = True,
        diagonal: bool = True,
    ) -> Union[List[Tuple[int, int]], List[str]]:
        """
        Get the adjacent fields of a given index

        Args:
            i: row index
            j: column index
            diagonal: include diagonal fields
            as_values: return values instead of indices

        Returns:
            List of indices (tuples) or values (strings)
        """
        indices = []
        if horizontal_vertical:
            indices += [(i - 1, j), (i, j - 1), (i, j + 1), (i + 1, j)]
        if diagonal:
            indices += [(i - 1, j - 1), (i - 1, j + 1), (i + 1, j - 1), (i + 1, j + 1)]
        if as_values:
            return self.fields_to_values(indices)
        return indices

    def __repr__(self):
        return "\n".join(["".join(line) for line in self.data])
