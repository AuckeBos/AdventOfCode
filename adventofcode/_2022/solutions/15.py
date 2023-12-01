import re
from typing import Dict

from src._2022.puzzle_to_solve import PuzzleToSolve


class Network:
    PATTERN = 'Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)'
    sensor_to_beacon: Dict[tuple, tuple]

    def __init__(self, input_: str):
        self.parse_input(input_)

    def parse_input(self, input_: str):
        positions = [[int(g) for g in re.match(self.PATTERN, line).groups()] for line in input_.split("\n")]
        sensor_to_beacon = {}
        for x_sensor, y_sensor, x_beacon, y_beacon in positions:
            sensor_to_beacon[(x_sensor, y_sensor)] = (x_beacon, y_beacon)
        self.sensor_to_beacon = sensor_to_beacon

    def check_row(self, y):
        horizontal_positions = set()
        for sensor, beacon in self.sensor_to_beacon.items():
            can_view = self.distance(sensor, beacon)
            horizontal_margin = can_view - self.distance(sensor, (sensor[0], y))
            if horizontal_margin > 0:
                horizontal_positions.update(range(-horizontal_margin + sensor[0], horizontal_margin + sensor[0] + 1))
        invalid_xs = [s[0] for s in self.sensor_to_beacon.values() if s[1] == y]
        valid_xs = list(set(horizontal_positions) - set(invalid_xs))
        return valid_xs

    def distance(self, point1, point2):
        return sum(abs(value1 - value2) for value1, value2 in zip(point1, point2))


class Puzzle15(PuzzleToSolve):

    @property
    def day(self) -> int:
        return 15

    @property
    def test_input(self) -> str:
        return """Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3"""

    @property
    def test_answer_a(self):
        return 26

    @property
    def test_answer_b(self):
        return 56000011

    def test_a(self):
        network = Network(self.test_input)
        items = network.check_row(10)
        return len(items)

    def a(self, input_: str):
        network = Network(input_)
        items = network.check_row(2000000)

        return len(items)

    def test_b(self):
        max_val = 21
        network = Network(self.test_input)
        for y in range(1, max_val):
            xs = network.check_row(y)
            xs = list(set(range(1, max_val)) - set(xs))
            if len(xs) > 0:
                x = xs[0]
                if (x, y) in network.sensor_to_beacon.keys() or (x, y) in network.sensor_to_beacon.values():
                    continue
                return x * 4000000 + y

    def b(self, input_: str):
        max_val = 4000001
        network = Network(input_)
        for y in range(1, max_val):
            xs = network.check_row(y)
            xs = list(set(range(1, max_val)) - set(xs))
            if len(xs) > 0:
                x = xs[0]
                if (x, y) in network.sensor_to_beacon.keys() or (x, y) in network.sensor_to_beacon.values():
                    continue
                return x * 4000000 + y


puzzle = Puzzle15()
puzzle.solve()
