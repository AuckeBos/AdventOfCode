from itertools import product
from typing import List, Tuple

import numpy as np
from numpy.typing import NDArray


def parse_matrix(input: str, as_int: bool = False) -> NDArray:
    """
    Matrix as text to matrix as ndarray
    :param input: Input matrix as string
    :param as_int: If true, cast elements to int, else to string
    :return: NDArray
    """
    cast = int if as_int else str
    return np.array([np.array([cast(i) for i in list(r)]) for r in input.splitlines()])


def neighbours(
        matrix: NDArray, r: int, c: int, allow_diagonal: True
) -> List[Tuple[int, int]]:
    """
    Get the neighbours of a point in a mtrix
    :param matrix: The matrix
    :param r: Current row
    :param c: Cuurent col
    :param allow_diagonal: Allow diagonal neighbours
    :return: List[Tuple[int,int]] Of neighbouring values
    """

    def valid(ri: int, ci: int):
        return (
                not (ri == r and ci == c)  # no self
                and 0 <= ri < matrix.shape[0]  # within bounds
                and 0 <= ci < matrix.shape[1]  # within bounds
        )

    if allow_diagonal:
        indices = product([-1, 0, 1], [-1, 0, 1])
        indices = [(ri + r, ci + c) for ri, ci in indices]
    else:
        indices = [
            (r, c - 1),
            (r - 1, c),
            (r, c + 1),
            (r + 1, c),
        ]
    return [(ri, ci) for ri, ci in indices if valid(ri, ci)]


def xys_to_rcs(x_start: int | str, y_start: int | str, x_end: int | str = None, y_end: int | str = None) -> Tuple[
    range, range]:
    """
    Convert x,y coordinates to row,column coordinates (eg puzzle values to numpy indices)
    Parameters
    ----------
    x_start, y_start: int, int
        The x and y position
    x_end, y_end: int, int
        If want to convert a row/column of indices, this is the other end of the row/column. Ordering of both points
        does not matter

    Returns
    -------
    Tuple[range, range]: The row indices, the column indices. Can be used for indexing on numpy arrays
    """
    x_end = x_end or x_start
    y_end = y_end or y_start

    x_start, x_end = sorted([int(x_start), int(x_end)])
    y_start, y_end = sorted([int(y_start), int(y_end)])

    x_end += 1
    y_end += 1

    return range(y_start, y_end), range(x_start, x_end)
