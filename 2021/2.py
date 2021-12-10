from typing import List, Tuple

from aocd.models import Puzzle


def get_count(lines: List[int], window: int):
    count = 0
    for i in range(1, len(lines)):
        curr_sum = sum(lines[i : i + window])
        prev_sum = sum(lines[i - 1 : i + window - 1])
        if curr_sum > prev_sum:
            count += 1
    return count


def pt_1(lines: List[Tuple[str, str]]):
    h = 0
    d = 0
    for dr, va in lines:
        va = int(va)
        if dr == "forward":
            h += va
        if dr == "up":
            d -= va
        if dr == "down":
            d += va
    return h * d


def pt_2(lines: List[Tuple[str, str]]):
    h = 0
    d = 0
    a = 0
    for dr, va in lines:
        va = int(va)
        if dr == "forward":
            h += va
            d += a * va
        if dr == "up":
            a -= va
        if dr == "down":
            a += va
    return h * d


puzzle = Puzzle(year=2021, day=2)
lines = puzzle.input_data.splitlines()
lines = [l.split(" ") for l in lines]

puzzle.answer_a = pt_1(lines)
puzzle.answer_b = pt_2(lines)
