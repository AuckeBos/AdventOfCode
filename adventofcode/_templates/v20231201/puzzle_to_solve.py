from abc import ABC, abstractmethod
from aocd.models import Puzzle
import datetime

class PuzzleToSolve(ABC):
    """
    Implement this class to solve a puzzle
    """
    puzzle: Puzzle

    def __init__(self) -> None:
        """
        Upon init, set the puzzle. Year is _2022. Day is provided as class property
        """        
        self.puzzle = Puzzle(self.year, self.day)
        super().__init__()


    @property
    @classmethod
    def day(cls) -> int:
        """
        The day of the puzzle 
        """
        return None
    
    @property
    @classmethod
    def year(cls) -> int:
        """
        The year of the puzzle 
        """
        return None

    @property
    @abstractmethod
    def test_input(self) -> str:
        """
        The test input string. Provided in the puzzle description 
        """
        pass

    @property
    def test_input_alternative(self) -> str:
        """
        The alternative test input. Some puzzles have alternative inputs for b). In those cases, this method should 
        be overridden. By default return test_input
        """
        return self.test_input


    @property
    @abstractmethod
    def test_answer_a(self):
        """
        The answer to question a, given the test input. Provided in the puzzle description
        """
        pass


    @property
    @abstractmethod
    def test_answer_b(self):
        """
        The answer to question b, given the test input. Provided in the puzzle description
        """
        pass


    @abstractmethod
    def a(self, input_: str):
        """
        Returns the solution to puzzle a, given the actual input.
        """
        pass


    @abstractmethod
    def b(self, input_: str):
        """
        Returns the solution to puzzle b, given the actual input.
        """
        pass

    def test_a(self):
        return self.a(self.test_input)

    def test_b(self):
        return self.b(self.test_input_alternative)

    def solve_exercise(self, name: str):
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
        if name not in ['a', 'b']:
            raise ValueError(f'Cannot solve exercise {name}')
        expected = getattr(self, f'test_answer_{name}')
        got = getattr(self, f'test_{name}')()

        if not expected == got:
            raise AssertionError(f'Cannot solve {name}: The test input answer is {expected}, while {name}() returned {got}')

        puzzle_input = self.puzzle.input_data
        answer = getattr(self, name)(puzzle_input)
        setattr(self.puzzle, f'answer_{name}', answer)


    def solve(self):
        """
        Solve both a) and b)
        """
        self.solve_exercise('a')
        print("Solved puzzle A")
        self.solve_exercise('b')
        print("Solved puzzle B")
