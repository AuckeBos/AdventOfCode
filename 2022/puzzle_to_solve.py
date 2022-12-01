from abc import ABC, abstractmethod
from aocd.models import Puzzle

class PuzzleToSolve(ABC):
    puzzle: Puzzle
    def __init__(self) -> None:
        self.puzzle = Puzzle(2022, self.day)
        super().__init__()
    
    @property
    def day(cls) -> int:
        pass

    @property
    @abstractmethod
    def test_input(self) -> str:
        pass

    @property
    @abstractmethod
    def test_answer_a(self):
        pass
    
    @property
    @abstractmethod
    def test_answer_b(self):
        pass
    
    @abstractmethod
    def a(self, input: str):
        pass

    @abstractmethod
    def b(self, input: str):
        pass


    def solve_excercise(self, name: str):
        if name not in ['a', 'b']:
            raise Exception(f'Cannot solve excercise {name}')
        input = self.test_input
        expected = self.__getattribute__(f'test_answer_{name}')
        got = self.__getattribute__(name)(input)
        if not expected == got:
            raise Exception(f'Cannot solve {name}: The test input answer is {expected}, while {name}() returned {got}')
        
        input = self.puzzle.input_data
        answer = self.__getattribute__(name)(input)
        self.__setattr__(f'puzzle.answer_{name}', answer)

    def solve(self):
        self.solve_excercise('a')
        print("Solved puzzle A")
        self.solve_excercise('b')
        print("Solved puzzle B")