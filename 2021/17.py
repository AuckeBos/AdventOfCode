import re
from typing import Tuple, List

from aocd.models import Puzzle


def parse_input(text: str) -> Tuple[range, range]:
    pattern = "target area: x=(-?\d+)\.\.(-?\d+)+, y=(-?\d+)+\.\.(-?\d+)+"
    values = [int(v) for v in re.match(pattern, text).groups()]
    x_t = range(values[0], values[1] + 1)
    y_t = range(values[2], values[3] + 1)
    return x_t, y_t


def step(x: int, y: int, x_v: int, y_v: int) -> Tuple[int, int, int, int]:
    x += x_v
    y += y_v
    x_v += 1 if x_v < 0 else (-1 if x_v != 0 else 0)
    y_v -= 1
    return x, y, x_v, y_v


def target_achieved(x: int, y: int, x_t: range, y_t: range) -> bool:
    return x in x_t and y in y_t


def target_exceeded(x: int, y: int, x_t: range, y_t: range) -> bool:
    return x > x_t[-1] or y < y_t[0]


def try_one(x: int, y: int, x_t: range, y_t: range, x_v: int, y_v: int) -> bool:
    while not target_exceeded(x, y, x_t, y_t):
        x, y, x_v, y_v = step(x, y, x_v, y_v)
        if target_achieved(x, y, x_t, y_t):
            return True
    return False


def try_many(
    x: int, y: int, x_t: range, y_t: range, x_v_range: list, y_v_range: list
) -> List[Tuple[int, int]]:
    result = []
    for x_v in x_v_range:
        for y_v in y_v_range:
            if try_one(x, y, x_t, y_t, x_v, y_v):
                result.append((x_v, y_v))
    return result


def get_y_v_options(y_t: range):
    """
    The options for y_v are not dependent on x_v
    :param y_t: target y
    :return: y_v options
    """
    result = []
    for y_v in range(1000, -1000, -1):
        if try_one(0, 0, range(1), y_t, 0, y_v):
            result.append(y_v)
    return result


puzzle = Puzzle(year=2021, day=17)
x_t, y_t = parse_input(puzzle.input_data)

y_v_range = get_y_v_options(y_t)
x_v_range = list(range(0, 1000))
result = try_many(0, 0, x_t, y_t, x_v_range, y_v_range)
puzzle.answer_a = sum(range(result[0][1] + 1))
puzzle.answer_b = len(result)
