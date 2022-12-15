from abc import ABC, abstractmethod
from aocd.models import Puzzle


class PuzzleToSolve(ABC):
    """
    Implement this class to solve a puzzle
    """
    puzzle: Puzzle
    """
    Upon init, set the puzzle. Year is _2022. Day is provided as class property
    """

    def __init__(self) -> None:
        self.puzzle = Puzzle(2022, self.day)
        super().__init__()

    """
    The day of the puzzle 
    """

    @property
    @abstractmethod
    def day(cls) -> int:
        return None

    """
    The test input string. Provided in the puzzle description 
    """

    @property
    @abstractmethod
    def test_input(self) -> str:
        pass

    """
    The alternative test input. Some puzzles have alternative inputs for b). In those cases, this method should 
    be overridden. By default return test_input
    """

    @property
    def test_input_alternative(self) -> str:
        return self.test_input

    """
    The answer to question a, given the test input. Provided in the puzzle description
    """

    @property
    @abstractmethod
    def test_answer_a(self):
        pass

    """
    The answer to question b, given the test input. Provided in the puzzle description
    """

    @property
    @abstractmethod
    def test_answer_b(self):
        pass

    """
    Returns the solution to puzzle a, given the actual input.
    """

    @abstractmethod
    def a(self, input_: str):
        pass

    """
    Returns the solution to puzzle b, given the actual input.
    """

    @abstractmethod
    def b(self, input_: str):
        pass

    def test_a(self):
        return self.a(self.test_input)

    def test_b(self):
        return self.b(self.test_input)
    """
    Solve an exercise:
    - Run the implementation, given the test input.
    - Assert that the answer to the test input is correct
    - Run the implementation, given the actual input
    - Submit the result
    Parameters
    ----------
    name: str
        The name of the puzzle to solve. Should be 'a' or 'b'
    """

    def solve_exercise(self, name: str, test_input: str):
        if name not in ['a', 'b']:
            raise Exception(f'Cannot solve excercise {name}')
        expected = self.__getattribute__(f'test_answer_{name}')
        got = self.__getattribute__(f'test_{name}')()

        if not expected == got:
            raise Exception(f'Cannot solve {name}: The test input answer is {expected}, while {name}() returned {got}')

        input = self.puzzle.input_data
        answer = self.__getattribute__(name)(input)
        self.puzzle.__setattr__(f'answer_{name}', answer)

    """
    Solve both a) and b)
    """

    def solve(self):
        self.solve_exercise('a', self.test_input)
        print("Solved puzzle A")
        self.solve_exercise('b', self.test_input_alternative)
        print("Solved puzzle B")
