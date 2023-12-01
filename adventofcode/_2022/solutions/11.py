import re
from functools import reduce
from math import gcd
from typing import List, Callable

from src._2022.puzzle_to_solve import PuzzleToSolve


class Monkey:
    """
    A Monkey is defined by the following attributes:
    items: List[int]
        List of worry_level values of the items the monkey holds
    operation: Callable[[int], int]
        The operation to be performed on 'old' (param), to compute 'new' (result)
    test: Callable[[int], bool]
        The test to perform on 'worry level' (param), return True if succeeds else False
    test_succeeds_monkey: int
        The index of the monkey to pass the item to, if test(worry_level) == True
    test_fails_monkey: int
        The index of the monkey to pass the item to, if test(worry_level) == False
    inspection_count: int
        The amount of inspections the monkey has taken. Is increased by the game, each time the Monkey takes a turn
    divisor: int
        Used in test(), to test whether the worry level is divisible. Moreover, used to compute gcd() of all divisors,
        to prevent very large worry levels
    pattern: str
        Static regex pattern to extract the relevant values from a string repr of a monkey

    """
    items: List[int]
    operation: Callable[[int], int]
    test: Callable[[int], bool]
    test_succeeds_monkey: int
    test_fails_monkey: int
    inspection_count: int = 0
    divisor: int

    pattern = "Monkey \d+:\n  Starting items: (.*)\n  Operation: new = (.*)\n  Test: divisible by (\d+)\n    If true: throw to monkey (\d+)\n    If false: throw to monkey (\d+)"

    def __init__(self, input_: str):
        self.parse_input(input_)

    def parse_input(self, input_: str):
        """
        Parse the input, setting variables accordingly:
        - Use pattern to get values
        - self.items[] is the str.splitted integer value
        - self.operation: use math.eval() to return the evaluated value of the string
        - self.divisor: The value used in test(), if worry level mod divisor is 0, test succeeds
        - The test, as a lambda. Consumes worry level and returns true if it is divisible by divisor
        - test_{succeeds|fails}_monkey: To which monkey to pass if test is True/False
        """
        groups = re.search(self.pattern, input_).groups()
        items_str, operation_str, test_str, test_succeeds_str, test_fails_str = groups
        self.items = [int(x) for x in items_str.split(', ')]
        self.operation = lambda old: eval(operation_str)
        self.divisor = int(test_str)
        self.test = lambda v: v % self.divisor == 0
        self.test_succeeds_monkey = int(test_succeeds_str)
        self.test_fails_monkey = int(test_fails_str)


class KeepAway:
    monkeys: List[Monkey]
    extreme_worry: bool
    lcm: int

    def __init__(self, input_: str, extreme_worry: bool):
        self.extreme_worry = extreme_worry
        self.parse_input(input_)

    def parse_input(self, input_: str):
        """
        - Parse the input, creating a list of monkeys
        - Save the LCM of all monkey.divisors in self
        """
        monkeys_str = input_.split("\n\n")
        self.monkeys = [Monkey(monkey_str) for monkey_str in monkeys_str]
        self.lcm = self.compute_lcm([m.divisor for m in self.monkeys])

    def play_monkey(self, monkey: Monkey):
        """
        Play the turn of a monkey:
        - For each item
            - Increase inspection count
            - Apply operation to get new worry level.
            - If not exteremely worried (part a)), divide the worry level by 3.
            - Else, to not divide it. However, take mod using self.lcm. This prevents extreme worry levels,
                but has no influence on the test() of any of the monkeys
            - Get monkey to pass the item to
            - Pass the item to the monkey
        - Remove all items from the monkey (it passes all items after it is bored with them)
        """
        items = monkey.items.copy()
        for item in monkey.items:
            monkey.inspection_count += 1
            new_worry_level = monkey.operation(item)
            if not self.extreme_worry:
                new_worry_level //= 3
            else:
                new_worry_level = new_worry_level % self.lcm
            new_monkey_index = monkey.test_succeeds_monkey if monkey.test(new_worry_level) else monkey.test_fails_monkey
            new_monkey = self.monkeys[new_monkey_index]
            new_monkey.items.append(new_worry_level)
        monkey.items = monkey.items[len(items):]

    def play_round(self):
        for monkey in self.monkeys:
            self.play_monkey(monkey)

    def play_rounds(self, n: int):
        for i in range(n):
            self.play_round()

    @property
    def monkey_business(self):
        """
        The monkey business is the mult of the two highest inspection counts
        """
        inspection_counts = [monkey.inspection_count for monkey in self.monkeys]
        inspection_counts.sort(reverse=True)
        return inspection_counts[0] * inspection_counts[1]

    def compute_lcm(self, ints: List[int]):
        """
        Use math.gcd to compute the lcm of a list of ints
        """
        return reduce(lambda a, b: a * b // gcd(a, b), ints)


class Puzzle11(PuzzleToSolve):
    @property
    def day(self) -> int:
        return 11

    @property
    def test_input(self) -> str:
        return """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1"""

    @property
    def test_answer_a(self):
        return 10605

    @property
    def test_answer_b(self):
        return 2713310158

    def a(self, input_: str):
        """
        Compute a):
        - Create a game without extreme worryness
        - Play the game for 20 rounds
        - Return the monkey_business of the game
        """
        game = KeepAway(input_, False)
        game.play_rounds(20)
        result = game.monkey_business
        return result

    def b(self, input_: str):
        """
        Compute a):
        - Create a game with extreme worryness
        - Play the game for 10000 rounds
        - Return the monkey_business of the game
        """
        game = KeepAway(input_, True)
        game.play_rounds(10000)
        result = game.monkey_business
        return result


puzzle = Puzzle11()
puzzle.solve()
