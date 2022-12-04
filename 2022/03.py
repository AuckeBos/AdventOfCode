from puzzle_to_solve import PuzzleToSolve
import string

class Puzzle4(PuzzleToSolve):
    item_types = [*string.ascii_lowercase, *string.ascii_uppercase]
    @property
    def day(self) -> int:
        return 3

    @property
    def test_input(self) -> str:
        return """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw"""

    @property
    def test_answer_a(self):
        return 157

    @property
    def test_answer_b(self):
        return 70

    def get_priority(self, item_type: str):
        if item_type not in self.item_types:
            raise Exception(f'{item_type} is an invalid item type')
        return self.item_types.index(item_type) + 1



    """
    Solve a:
    - 
    """
    def a(self, input: str) -> int:
        bags = input.split('\n')
        result = 0
        for bag in bags:
            total = len(bag)
            half = total // 2
            left, right = bag[:half], bag[half:]
            duplicate = list(set(left) & set(right))[0]
            result += self.get_priority(duplicate)


        return result

    """
    Solve b:
    - 
    """
    def b(self, input: str) -> int:
        bags = input.split('\n')
        groups = [bags[i:i + 3] for i in range(0, len(bags), 3)]
        result = 0
        for group in groups:
            duplicate = list(set(group[0]) & set(group[1]) & set(group[2]))[0]
            result += self.get_priority(duplicate)
        return result


puzzle = Puzzle4()
puzzle.solve()
