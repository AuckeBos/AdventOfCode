from typing import List, Tuple
from adventofcode._templates.v20231204.puzzle_to_solve import PuzzleToSolve
from functools import cache

class Puzzle12(PuzzleToSolve):
    @property
    def day(self) -> int:
        return 12
    
    @property
    def year(self) -> int:
        return 2023

    @property
    def test_input(self) -> str:
        return """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""

    @property
    def test_answer_a(self):
        return 21

    @property
    def test_answer_b(self):
        return 525152

    def parse_input(self, input_: str) -> List[Tuple[str, List[int]]]:
        """
        Parse the input into a list of tuples. Each tuple is the string of chars, followed by a list of digits.
        """
        lines = input_.split("\n")
        data = []
        for line in lines:
            chars, digits = line.split(" ")
            digits = [int(d) for d in digits.split(",")]
            data.append((chars, digits))
        return data
    
    # This annotation makes b) possible.
    @cache
    def nr_of_possibilities(self, springs: str, groups: tuple, allow_damaged: bool = True, allow_operational: bool = True) -> int:
        """
        Find the number of possible arrangements for the given springs and groups.
        
        :param springs: The springs that are to be checked.
        :param groups: The groups of damaged springs.
        :param allow_damaged: Whether the first spring is allwoed to be damaged.
        :param allow_operational: Whether the first spring is allowed to be operational.
        
        :return: The number of possible arrangements.
        
        """
        # No more springs left
        if not springs:
            # We have a match if there need to be no more damaged springs
            if not len(groups):
                return 1
            # More damaged springs are needed, while there are none. No match.
            return 0
        # Pop the first spring
        spring = springs[0]
        springs = springs[1:]
        if spring == "#":
            # If we have an unallowed damaged spring, or we have a damaged spring, but there are no more damaged springs expected, no match
            if not allow_damaged or not len(groups):
                return 0
            new_group = groups[0] - 1
            groups = groups[1:]
            # This if should never be true
            if new_group < 0:
                raise ValueError("Group of length 0")
            # If we still expect more damaged springs in this group
            if new_group > 0:
                # Re-insert the decremented group
                groups = (new_group, *groups)
                # We expect more damaged springs in the current group. Hence damaged is allowed, but operational is not
                allow_damaged = True
                allow_operational = False
            else:
                # This was the last damaged spring in the current group. Hence damaged is not allowed, but operational is
                allow_damaged = False
                allow_operational = True
            # Return the nr of possible arrangements for the remaining springs and groups
            return self.nr_of_possibilities(springs, tuple(groups), allow_damaged, allow_operational)
        if spring == ".":
            # If we have an unallowed operational spring, no match
            if not allow_operational:
                return 0
            # Return the number of possible arrangements for the remaining springs and groups. Because we currently have an operational, both damaged and operational are allowed
            return self.nr_of_possibilities(springs, tuple(groups), True, True)
        if spring == "?":
            # Sum the number of possible arrangements for both options: damaged and operational
            return self.nr_of_possibilities(f".{springs}", tuple(groups), allow_damaged, allow_operational) + self.nr_of_possibilities(f"#{springs}", tuple(groups), allow_damaged, allow_operational)
            

    def a(self, input_: List[Tuple[str, List[int]]]) -> int:
        """
        Sum the number of possible arrangements for each line.
        """
        return sum([self.nr_of_possibilities(chars, tuple(digits)) for chars, digits in input_])

    def b(self, input_: List[Tuple[str, List[int]]]) -> int:
        """
        Unfold, and use a.
        Possible because nr_of_possibilities is cached.
        """
        unfolded_input = [('?'.join([chars for _ in range(5)]), digits * 5) for chars, digits in input_]
        return self.a(unfolded_input)


puzzle = Puzzle12()
puzzle.solve()
