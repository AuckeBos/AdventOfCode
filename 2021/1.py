from typing import List

from aocd.models import Puzzle


def get_count(lines: List[int], window: int):
    count = 0
    for i in range(1, len(lines)):
        curr_sum = sum(lines[i : i + window])
        prev_sum = sum(lines[i - 1 : i + window - 1])
        if curr_sum > prev_sum:
            count += 1
    return count


puzzle = Puzzle(year=2021, day=1)
lines = [int(x) for x in puzzle.input_data.splitlines()]
puzzle.answer_a = get_count(lines, 1)
puzzle.answer_b = get_count(lines, 3)
