from collections import defaultdict
from adventofcode._templates.puzzle_to_solve import PuzzleToSolve
import re

class Puzzle4(PuzzleToSolve):
    @property
    def day(self) -> int:
        return 4
    
    @property
    def year(self) -> int:
        return 2023

    @property
    def test_input(self) -> str:
        return """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""

    @property
    def test_answer_a(self):
        return 13

    @property
    def test_answer_b(self):
        return 30
    
    def get_matches(self, input_: str):
        """
        Get the matches between the winning numbers and the own numbers.
        Result is a list of sets, where each set contains the numbers that match in that scratch card
        """
        regex = r"Card \d+: (.*) \| (.*)"
        matches = []
        for line in input_.splitlines():
            # Remove double spaces
            line = re.compile(r"\s+").sub(" ", line)
            if not re.match(regex, line):
                raise ValueError(f"Invalid line: {line}")
            winning, own = re.search(regex, line).groups()
            winning_nrs = [int(x) for x in winning.split()]
            own_nrs = [int(x) for x in own.split()]
            matches.append(set(winning_nrs).intersection(set(own_nrs)))
        return matches

    def a(self, input_: str):
        """
        Sum the points of each card. A point scores 2^(n-1) points, where n is the number of matches
        """
        data = self.get_matches(input_)
        points = []
        for matches in data:
            points.append(int(2**(len(matches) - 1)) if matches else 0)
        return sum(points)

    def b(self, input_: str):
        """
        Count the total nr of scratch cards. Each card duplicates the n cards after it, where n is the number of matches
        """
        data = self.get_matches(input_)
        # One original card for each
        counts = {str(i): 1 for i in range(len(data))}
        for i, matches in enumerate(data):
            for j in range(1, len(matches) + 1):
                # Increase the count for the jth card after i, with the count (original + copy) of the ith card
                counts[str(i + j)] += counts[str(i)]
        return sum(counts.values())


puzzle = Puzzle4()
puzzle.solve()
