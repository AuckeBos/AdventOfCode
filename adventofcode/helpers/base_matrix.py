import numpy as np


class BaseMatrix:
    """
    Matrix class, to be used as a base class for other matrix classes
    Parses input into a numpy matrix, and provides some helper functions
    """
    data: np.ndarray
    
    def parse_input(self, input_: str, pad: str = "."):
        """
        Input string to numpy matrix. Surround matrix with pad, to make sure we don't get index errors
        """
        # Create numpy character matrix from input
        self.data = np.array([list(line) for line in input_.split("\n")])
        # Surround matrix with ".", to make sure we don't get index errors
        self.data = np.pad(self.data, 1, constant_values=pad)
    
    def iter_topleft_to_bottomright(self):
        """
        Yield all indices from top left to bottom right
        """
        for i in range(1, self.data.shape[0] - 1):
            for j in range(1, self.data.shape[1] - 1):
                yield i, j
    
    def adjacent_fields(self, i: int, j: int):
        """
        Get the adjacent fields of a given index
        """
        return [
            (i - 1, j - 1), (i - 1, j), (i - 1, j + 1),
            (i, j - 1), (i, j + 1),
            (i + 1, j - 1), (i + 1, j), (i + 1, j + 1)
        ]