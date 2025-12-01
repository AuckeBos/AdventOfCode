from itertools import accumulate
from typing import Literal

from adventofcode._templates.v20231204.puzzle_to_solve import PuzzleToSolve


class Puzzle1(PuzzleToSolve):
    @property
    def day(self) -> int:
        return 1

    @property
    def year(self) -> int:
        return 2025

    @property
    def test_input(self) -> str:
        return """L68
L30
R48
L5
R60
L55
L1
L99
R14
L82"""

    @property
    def test_answer_a(self) -> int:
        return 3

    @property
    def test_answer_b(self) -> int:
        return 6

    def parse_input(self, input_: str) -> list[tuple[Literal["L", "R"], int]]:
        return [(line[0], int(line[1:])) for line in input_.splitlines()]  # type: ignore

    def a(self, input_: list[tuple[Literal["L", "R"], int]]) -> int:
        return sum(
            1  # convert accums to count-zeros
            for pos in accumulate(  # Loop over each, returning state after each step
                input_,  # Loop over all steps
                lambda accumulated, current: (accumulated - current[1])
                % 100  # apply step, return state after step
                if current[0] == "L"
                else (accumulated + current[1]) % 100,
                initial=50,  # start at 50
            )
            if pos == 0  # Only count if current pos is 0
        )

    def b(self, input_: list[tuple[Literal["L", "R"], int]]) -> int:
        return sum(  # Sum the number of 0-passes
            item[1]  # item is (pos, passes)
            for item in accumulate(  # Loop over each, returning (state, passes) after each step
                input_,
                lambda accumulated,
                current: (  # accumulated = (previous_state, previous_passes)
                    (
                        (
                            (accumulated[0] - current[1]) % 100  # apply step to state
                            if current[0] == "L"
                            else (accumulated[0] + current[1]) % 100
                        ),
                        (
                            abs(  # compute number of zero-passes in this step
                                (
                                    (accumulated[0] - current[1])
                                    if current[0] == "L"
                                    else (accumulated[0] + current[1])
                                )
                                // 100
                            )
                        ),
                    )
                ),
                initial=(50, 0),  # start at (50, 0)
            )
        )


puzzle = Puzzle1()
puzzle.solve()
