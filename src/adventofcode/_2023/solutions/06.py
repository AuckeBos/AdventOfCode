from collections import defaultdict
from typing import Dict
from adventofcode._templates.v20231204.puzzle_to_solve import PuzzleToSolve
import re
import math

class Puzzle6(PuzzleToSolve):
    @property
    def day(self) -> int:
        return 6
    
    @property
    def year(self) -> int:
        return 2023

    @property
    def test_input(self) -> str:
        return """Time:      7  15   30
Distance:  9  40  200"""

    @property
    def test_answer_a(self) -> int:
        return 288

    @property
    def test_answer_b(self) -> int:
        return 71503

    def parse_input(self, input_: str) -> Dict[int, int]:
        """
        Split the input into two lists, then zip them together into a dict
        
        Returns:
            Dict[int, int]: A dict of time to distance
        """
        regex = "Time: +((?:\d+ *)+)\nDistance: +((?:\d+ *)+)"
        times, distances = re.match(regex, input_).groups()
        times = [int(x) for x in times.split()]
        distances = [int(x) for x in distances.split()]
        return dict(zip(times, distances))
    
    def compute_all_distances(self):
        """
        For each game where the time is between 0 and 1000,
        Compute all the distances that can be achieved.
        
        Returns:
            Dict[int, Dict[int, int]]: A dict of time to a dict of charge to distance
        """
        distances = defaultdict(lambda: {})
        for max_time in range(0, 1000):
            for charge in range(0, 1000):
                speed_after_charge = charge
                time_remaining = max_time - charge
                distance = speed_after_charge * time_remaining
                distances[max_time][charge] = distance
        return distances
            

    def a(self, time_to_distance: Dict[int, int]) -> int:
        """
        For each game, compute the number of options that travel further than the current record.
        
        Returns:
            int: The product of number of games that travel further than the record for each game
        """
        all_distances = self.compute_all_distances()
        return math.prod(
            [
                len([o for o in all_distances[time].values() if o > record]) for time, record in time_to_distance.items()
            ]
        )

    def b(self, time_to_distance: Dict[int, int]) -> int:
        """
        Glue all the times and distances together, into one game.
        For all possible charge values, compute the distance travelled.
        
        Returns:
            int: The number of times the distance is further than the current record
        """
        time = int(''.join([str(x) for x in time_to_distance.keys()]))
        current_record = int(''.join([str(x) for x in time_to_distance.values()]))
        
        winning_strategies = 0
        for charge in range(0, time):
            speed_after_charge = charge
            time_remaining = time - charge
            distance = speed_after_charge * time_remaining
            if distance > current_record:
                winning_strategies += 1
        return winning_strategies


puzzle = Puzzle6()
puzzle.solve()
