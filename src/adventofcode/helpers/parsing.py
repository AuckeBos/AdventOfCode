from io import StringIO
from typing import Any, List

import numpy as np


def as_cols(input_: str, sep: str = " ", caster: callable = int) -> List[List[int]]:
    """
    Parses a string input into a list of columns.

    Args:
        input_ (str): The input string to parse.
        sep (str): The separator used in the input string. Default is a space.
        caster (callable): A function to cast the parsed values. Default is int.

    Returns:
        List[List[int]]: A list of columns, where each column is a list of casted values.
    """
    return (
        np.loadtxt(StringIO(input_.replace(sep, " ")), dtype=caster)
        .transpose()
        .tolist()
    )


def as_matrix(
    input_: str, sep: str = " ", caster: callable = int, padding: Any = 0
) -> np.matrix:
    """
    Parses a string input into a NumPy matrix.
    Try np.loadtxt. This fails for variable-length rows. In that case, fall back
    to manual array building and padding.

    Args:
        input_ (str): The input string to parse.
        sep (str): The separator used in the input string. Default is a space.
        caster (callable): A function to cast the parsed values. Default is int.
        padding (Any): The value to pad the matrix with. Default is 0.

    Returns:
        np.matrix: A NumPy matrix of casted values.
    """
    try:
        return np.loadtxt(StringIO(input_.replace(sep, " ")), dtype=caster)
    except ValueError:
        # Fallback for variable-length
        print("Reading input as variable-length rows, padding with", padding)
        data = [list(map(int, line.split())) for line in input_.split("\n")]
        max_cols = max(len(row) for row in data)
        return np.matrix([row + [padding] * (max_cols - len(row)) for row in data])
