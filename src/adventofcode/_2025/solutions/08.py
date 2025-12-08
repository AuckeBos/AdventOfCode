import itertools
from math import prod

from adventofcode._templates.v20231204.puzzle_to_solve import PuzzleToSolve


class Puzzle8(PuzzleToSolve):
    @property
    def day(self) -> int:
        return 8

    @property
    def year(self) -> int:
        return 2025

    @property
    def test_input(self) -> str:
        return """162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689"""

    @property
    def extra_kwargs(self) -> dict:
        """
        Extra kwargs to pass to the puzzle. Indexed on puzzle type
        """
        return {
            "a_test": {"num_connections": 10},
            "b_test": {},
            "a": {"num_connections": 1000},
            "b": {},
        }

    @property
    def test_answer_a(self) -> int:
        return 40

    @property
    def test_answer_b(self) -> int:
        return 25272

    def parse_input(self, input_: str) -> list[tuple[int, int, int]]:
        return sorted(
            [tuple(map(int, line.split(","))) for line in input_.splitlines()]
        )  # type: ignore

    def connect(
        self,
        circuits: list[list[tuple[int, int, int]]],
        a: tuple[int, int, int],
        b: tuple[int, int, int],
    ):
        """Connect two junction boxes into circuits."""
        circuit_a = next(
            (i for i, circuit in enumerate(circuits) if a in circuit), None
        )
        circuit_b = next(
            (i for i, circuit in enumerate(circuits) if b in circuit), None
        )
        # Both unmatched, add new circuit
        if circuit_a is None and circuit_b is None:
            circuits.append([a, b])
        # Add b to a's circuit
        elif circuit_a is not None and circuit_b is None:
            circuits[circuit_a].append(b)
        # Add a to b's circuit
        elif circuit_b is not None and circuit_a is None:
            circuits[circuit_b].append(a)
        # Both in some circuit
        elif circuit_a is not None and circuit_b is not None:
            # Not already in the same circuit: merge
            if circuit_a != circuit_b:
                circuits[circuit_a].extend(circuits[circuit_b])
                del circuits[circuit_b]
        else:
            raise ValueError("Unexpected case in circuit finding")

    def create_circuits_untill_max_circuits(
        self, junction_boxes: list[tuple[int, int, int]], num_connections: int
    ) -> list[list[tuple[int, int, int]]]:
        """Create circuits until the given number of connections is made.

        Args:
            junction_boxes: list of junction box coordinates
            num_connections: number of connections to make
        Returns:
            list of circuits created
        """
        distances = self.sort_on_distances(junction_boxes)
        circuits: list[list[tuple[int, int, int]]] = []
        num_connected = 0
        for _, (a, b) in distances:
            self.connect(circuits, a, b)
            num_connected += 1
            if num_connected >= num_connections:
                break
        return circuits

    def distance(self, a: tuple[int, int, int], b: tuple[int, int, int]) -> int:
        return abs(a[0] - b[0]) ** 2 + abs(a[1] - b[1]) ** 2 + abs(a[2] - b[2]) ** 2

    def sort_on_distances(
        self, points: list[tuple[int, int, int]]
    ) -> list[tuple[int, tuple[tuple[int, int, int], tuple[int, int, int]]]]:
        combinations = itertools.combinations(points, 2)
        return sorted(
            [(self.distance(a, b), (a, b)) for a, b in combinations], key=lambda x: x[0]
        )

    def a(self, junction_boxes: list[tuple[int, int, int]], num_connections: int):
        circuits = self.create_circuits_untill_max_circuits(
            junction_boxes, num_connections
        )
        circuits.sort(key=len, reverse=True)
        return prod(len(circuit) for circuit in circuits[:3])

    def create_circuits_until_single_circuit(
        self, junction_boxes: list[tuple[int, int, int]]
    ) -> int:
        """Create circuits until all junction boxes are connected into a single circuit.

        Args:
            junction_boxes: list of junction box coordinates
        Returns:
            The product of the X-coordinates of the last connected junction box before finish.
        """
        distances = self.sort_on_distances(junction_boxes)
        circuits: list[list[tuple[int, int, int]]] = []
        for _, (a, b) in distances:
            self.connect(circuits, a, b)
            if len(circuits) == 1 and len(circuits[0]) == len(junction_boxes):
                return a[0] * b[0]
        raise ValueError("Could not connect all junction boxes")

    def b(self, junction_boxes: list[tuple[int, int, int]]):
        return self.create_circuits_until_single_circuit(junction_boxes)


puzzle = Puzzle8()
puzzle.solve()
