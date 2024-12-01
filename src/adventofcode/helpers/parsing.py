from io import StringIO
from typing import List

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
