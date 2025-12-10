import re
import sys

from adventofcode._templates.v20231204.puzzle_to_solve import PuzzleToSolve


class GraphB:
    target: list[int]
    buttons: list[list[int]]
    history: dict[tuple[int, ...], int]  # ma states to steps

    def __init__(
        self, target: list[int], buttons: list[list[int]], joltage: list[int]
    ) -> None:
        self.target = joltage
        self.buttons = buttons
        self.history = {}

    def dfs(self, current: list[int]) -> int:
        if current == self.target:
            return 0
        if tuple(current) in self.history:
            return self.history[tuple(current)]
        if any(c > t for c, t in zip(current, self.target)):
            self.history[tuple(current)] = sys.maxsize
            return sys.maxsize
        self.history[tuple(current)] = sys.maxsize
        min_steps = sys.maxsize
        for button in self.buttons:
            next_state = [x + 1 if i in button else x for i, x in enumerate(current)]
            # while each next button press stays within target limits, press again
            pressed = 1
            while all(
                [
                    all(
                        n < t - 2
                        for n, t in zip(
                            [x + 1 if i in b else x for i, x in enumerate(next_state)],
                            self.target,
                        )
                    )
                    for b in self.buttons
                ]
            ):
                next_state = [
                    x + 1 if i in button else x for i, x in enumerate(next_state)
                ]
                pressed += 1
            steps = self.dfs(next_state)
            min_steps = min(min_steps, steps + pressed)
        self.history[tuple(current)] = min_steps
        return self.history[tuple(current)]


class Graph:
    target: list[int]
    buttons: list[list[int]]
    history: dict[tuple[int, ...], int]  # ma states to steps

    def __init__(
        self, target: list[int], buttons: list[list[int]], _: set[int]
    ) -> None:
        self.target = target
        self.buttons = buttons
        self.history = {}

    def dfs(self, current: list[int]) -> int:
        if current == self.target:
            return 0
        if tuple(current) in self.history:
            return self.history[tuple(current)]
        self.history[tuple(current)] = sys.maxsize
        min_steps = sys.maxsize
        for button in self.buttons:
            next_state = [x ^ 1 if i in button else x for i, x in enumerate(current)]
            steps = self.dfs(next_state)
            min_steps = min(min_steps, steps + 1)
        self.history[tuple(current)] = min_steps
        return self.history[tuple(current)]


class Puzzle10(PuzzleToSolve):
    @property
    def day(self) -> int:
        return 10

    @property
    def year(self) -> int:
        return 2025

    @property
    def test_input(self) -> str:
        return """[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"""

    @property
    def test_answer_a(self) -> int:
        return 7

    @property
    def test_answer_b(self) -> int:
        return 33

    def parse_input(
        self, input_: str
    ) -> list[tuple[list[int], list[list[int]], list[int]]]:
        regex = r"\[([.#]+)] ((?:\(\d+(?:,\d+)*\) )+){1}(\{(?:\d+(?:,\d+)*\)?)\})"
        result = []
        for line in input_.strip().split("\n"):
            target_str, buttons_str, joltage_str = re.match(
                regex, line.strip()
            ).groups()
            target = [int(c == "#") for c in target_str]
            buttons = [
                list(map(int, s[1:-1].split(",")))
                for s in buttons_str.strip().split(" ")
            ]
            joltage = [int(x) for x in joltage_str[1:-1].split(",")]
            result.append((target, buttons, joltage))
        return result

    def a(self, input_: list[tuple[list[int], list[list[int]], list[int]]]) -> int:
        sys.setrecursionlimit(10000)
        result = 0
        for line in input_:
            res = Graph(*line).dfs([0] * len(line[0]))
            result += res
        return result

    def b(self, input_: list[tuple[list[int], list[list[int]], list[int]]]) -> int:
        sys.setrecursionlimit(10000000)
        result = 0
        for i, line in enumerate(input_):
            res = GraphB(*line).dfs([0] * len(line[0]))
            result += res
            print(f"Line {i} done, result so far: {result}")

        return result


puzzle = Puzzle10()
puzzle.solve()
