from collections import defaultdict
from typing import List, Dict

from aocd.models import Puzzle


class Template:
    # Rules map origin 2gram to ngram, to to-be-inserted char
    rules: Dict[str, str]

    pair_counter: Dict[str, int]
    char_counter: Dict[str, int]

    def __init__(self, rules: List[str]):
        self.rules = {}
        self._build_rules(rules)

    def _build_rules(self, rules: List[str]):
        for rule in rules:
            l, r = rule.split(" -> ")
            self.rules[l] = r

    def _apply_once(self):
        for pair, count in self.pair_counter.copy().items():
            if pair in self.rules:
                new_char = self.rules[pair]
                self.pair_counter[pair[0] + new_char] += count
                self.pair_counter[new_char + pair[1]] += count
                self.pair_counter[pair] -= count
                self.char_counter[new_char] += count

    def apply(self, input: str, i: int):
        self.pair_counter = defaultdict(int)
        self.char_counter = defaultdict(int)
        for pair in [input[i : i + 2] for i in range(len(input) - 1)]:
            self.pair_counter[pair] += 1
        for c in input:
            self.char_counter[c] += 1
        for _ in range(i):
            self._apply_once()
        return self

    def get_score(self):
        score = max(self.char_counter.values()) - min(self.char_counter.values())
        return score


puzzle = Puzzle(year=2021, day=14)
template_str, rules = puzzle.input_data.split("\n\n")
template = Template(rules.splitlines())
puzzle.answer_a = template.apply(template_str, 10).get_score()
puzzle.answer_b = template.apply(template_str, 40).get_score()
