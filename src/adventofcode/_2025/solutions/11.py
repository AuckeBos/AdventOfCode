from collections import defaultdict
from typing import Generic, TypeVar

from adventofcode._templates.v20231204.puzzle_to_solve import PuzzleToSolve

T = TypeVar("T")


class Graph(Generic[T]):
    nodes: dict[T, list[T]]

    def __init__(self, devices: list[tuple[T, list[T]]]):
        self.nodes = defaultdict(list)
        for device, connections in devices:
            self.nodes[device] = connections

    def find_all_paths(
        self,
        start: T,
        end: T,
        visited: list[T] | None = None,
        visit_at_least: list[T] | None = None,
    ) -> list[list[T]]:
        """Find all paths from start to end node.

        Args:
            start (T): The starting node.
            end (T): The ending node.
            visited (list[T]): The current path.
        Returns:
            list[list[T]]: A list of all paths from start to end.
        """
        visit_at_least = visit_at_least or []
        visited = visited or []
        if start == end:
            return [visited + [end]]  # include end node in path
        if start not in self.nodes:
            return []
        visited.append(start)
        return [
            path
            for node in self.nodes[start]
            for path in self.find_all_paths(node, end, visited.copy())
            if all(v in path for v in visit_at_least)
        ]


class Puzzle11(PuzzleToSolve):
    @property
    def day(self) -> int:
        return 11

    @property
    def year(self) -> int:
        return 2025

    @property
    def test_input(self) -> str:
        return """aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out"""

    @property
    def test_input_alternative(self) -> str:
        return """svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out"""

    @property
    def test_answer_a(self) -> int:
        return 5

    @property
    def test_answer_b(self) -> int:
        return 2

    def parse_input(self, input_: str) -> list[tuple[str, list[str]]]:
        return [
            (line.split(": ")[0], line.split(": ")[1].split(" "))
            for line in input_.strip().split("\n")
        ]

    def a(self, devices: list[tuple[str, list[str]]]) -> int:
        return len(Graph(devices).find_all_paths("you", "out"))

    def b(self, devices: list[tuple[str, list[str]]]) -> int:
        # todo: this is too slow. need to prune early
        return len(
            Graph(devices).find_all_paths("svr", "out", visit_at_least=["fft", "dac"])
        )


puzzle = Puzzle11()
puzzle.solve()
