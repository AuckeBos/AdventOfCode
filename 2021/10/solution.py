from collections import defaultdict
from math import floor
from typing import List

import numpy as np


# PT1:
# PT2:
from aocd.models import Puzzle

syntax_score_map = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}

completion_score_map = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4,
}

char_map = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">",
}


def iterate(line: str, part: int):
    """
    Iterate the line. Return the desired result
    :param line: The line, string of opening and closing brackets
    :param part: 1 or 2
    :return: If part is 1: syntax score or 0. If part is 2: List of closing brackets
    that remain
    """
    openings = []
    for c in line:
        if c in char_map.keys():  # Is opening
            openings.append(c)
        else:  # Is closing
            o = openings.pop()
            # Closing does not match last opening. Part one: return syntax score
            if part == 1 and char_map[o] != c:
                return syntax_score_map[c]
    # Line not corrupted. Part 1: score is 0. Part 2: get closing brackets for remaining
    return 0 if part == 1 else [char_map[c] for c in reversed(openings)]


def get_completion_score(line: str):
    score = 0
    for c in iterate(line, 2):
        score = score * 5 + completion_score_map[c]
    return score


puzzle = Puzzle(year=2021, day=10)
data = np.array(puzzle.input_data.splitlines())
syntax_scores = np.array([iterate(l, 1) for l in data])
cum_syntax_scores = np.sum(syntax_scores)
puzzle.answer_a = cum_syntax_scores

corrupted_lines = data[syntax_scores == 0]
completion_scores = [get_completion_score(l) for l in corrupted_lines]
middle_score = sorted(completion_scores)[len(completion_scores) // 2]
puzzle.answer_b = middle_score
