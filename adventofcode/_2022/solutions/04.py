from src._2022.puzzle_to_solve import PuzzleToSolve


class Puzzle4(PuzzleToSolve):
    @property
    def day(self) -> int:
        return 4

    @property
    def test_input(self) -> str:
        return """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8"""

    @property
    def test_answer_a(self):
        return 2

    @property
    def test_answer_b(self):
        return 4

    """
    Solve a:
    - 
    """

    def a(self, input_: str) -> int:
        lst = input_.split("\n")
        pairs = [x.split(',') for x in lst]
        pairs_split = [[person.split('-') for person in pair] for pair in pairs]
        pairs_parsed = [[[int(side) for side in person] for person in duo] for duo in pairs_split]

        cnt = 0
        for pair in pairs_parsed:
            left_low = pair[0][0]
            left_high = pair[0][1]
            right_low = pair[1][0]
            right_high = pair[1][1]

            if (left_low <= right_low and left_high >= right_high) or (
                    right_low <= left_low and right_high >= left_high):
                cnt += 1
        return cnt

    """
    Solve b:
    - 
    """

    def b(self, input_: str) -> int:
        lst = input_.split("\n")
        pairs = [x.split(',') for x in lst]
        pairs_split = [[person.split('-') for person in pair] for pair in pairs]
        pairs_parsed = [[[int(side) for side in person] for person in duo] for duo in pairs_split]

        cnt = 0
        for pair in pairs_parsed:
            left_range = range(pair[0][0], pair[0][1] + 1)
            right_range = range(pair[1][0], pair[1][1] + 1)
            overlap = list(set(left_range) & set(right_range))
            if len(overlap) > 0:
                cnt += 1
        return cnt


puzzle = Puzzle4()
puzzle.solve()
