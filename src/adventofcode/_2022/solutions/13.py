import functools
import json
import math
from typing import List

from src._2022.puzzle_to_solve import PuzzleToSolve


class Puzzle13(PuzzleToSolve):
    @property
    def day(self) -> int:
        return 13

    @property
    def test_input(self) -> str:
        return """[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]"""

    @property
    def test_answer_a(self):
        return 13

    @property
    def test_answer_b(self):
        return 140

    @staticmethod
    def compair(left: int | List, right: int | list):
        """
        Compare two pairs. Return 0 if equal, 1 if left > right, -1 if left < right
        - If both int, return compare of int
        - If both are list, iterate items. If item comparison is not equal, return it. If both lists are of
            equal length and all items are equal, return equal. left size < right size and cant compare individual
            items, return -1. If size right < size left and all items equal, return 1
        - If one is list and other is int, convert in to singleton list of int, and return compare of both.
        """
        # Return int comparisson
        if type(left) == int and type(right) == int:
            return 0 if left == right else (1 if left > right else -1)
        # Iterate items
        if type(left) == list and type(right) == list:
            i = 0
            while i <= min(len(left), len(right)):
                # If both list exceeded and of same length, return equal
                if len(left) - 1 < i and len(right) - 1 < i:
                    return 0
                # If left size smaller than right size
                elif len(left) - 1 < i:
                    return -1
                # Other way around
                elif len(right) - 1 < i:
                    return 1
                # Compare next two items
                curr_comp = Puzzle13.compair(left[i], right[i])
                i += 1
                # If not equal, return result, else continue to next item pair
                if curr_comp != 0:
                    return curr_comp
            else:
                raise Exception("Both list iterated, and couldn't be compared")
        # Compare the int to a singleton list
        if type(left) == int:
            left = [left]
        elif type(right) == int:
            right = [right]
        else:
            raise Exception(f"Invalid invalid combination: {left}, {right}")
        # And return its comparison
        return Puzzle13.compair(left, right)

    def a(self, input_: str):
        """
        Solve a):
        - Convert input to list of pairs, each item is a list. Use json.loads to parse string to list
        - Compare each pair. If left < right, increase result by i+1 (1-indexing)
        - Return result
        """
        pairs_as_str = input_.split("\n\n")
        pairs_as_tuple = [pair.split("\n") for pair in pairs_as_str]
        pairs_parsed = [[json.loads(side) for side in pair] for pair in pairs_as_tuple]
        sum_indices_correctly_ordered_pairs = 0
        for i, (left, right) in enumerate(pairs_parsed):
            if self.compair(left, right) == -1:
                sum_indices_correctly_ordered_pairs += i + 1
        return sum_indices_correctly_ordered_pairs

    def b(self, input_: str):
        """
        Solve b):
        - Remove empty lines, convert to list of packets. Append the two divider packets
        - Sort the list, using compair
        - Find the indices of the divider packets (1-based indexing), and multiply them
        """
        input_wo_newlines = input_.replace("\n\n", "\n")
        divider_packets = [[[2]], [[6]]]
        packets = [json.loads(p) for p in input_wo_newlines.split("\n")] + divider_packets
        sorted_packets = sorted(packets, key=functools.cmp_to_key(self.compair))
        indexes = [sorted_packets.index(p) + 1 for p in divider_packets]
        result = math.prod(indexes)
        return result


puzzle = Puzzle13()
puzzle.solve()
