from puzzle_to_solve import PuzzleToSolve

class SolvedPuzzle(PuzzleToSolve):
    @property
    def day(self) -> int:
        return 1

    @property
    def test_input(self) -> str:
        return """1000
2000
3000

4000

5000
6000

7000
8000
9000

10000"""

    @property
    def test_answer_a(self):
        return 24000
        
    @property
    def test_answer_b(self):
        return 45000

    def a(self, input: str) -> int:
        elves = input.split("\n\n")
        elves_parsed = [elve.split("\n") for elve in elves]
        elves_cast = [[int(i) for i in elve] for elve in elves_parsed]
        elves_summed = [sum(elve) for elve in elves_cast]
        max_elve = max(elves_summed)
        return max_elve

    def b(self, input: str) -> int:
        elves = input.split("\n\n")
        elves_parsed = [elve.split("\n") for elve in elves]
        elves_cast = [[int(i) for i in elve] for elve in elves_parsed]
        elves_summed = [sum(elve) for elve in elves_cast]
        elves_summed.sort(reverse=True)
        top_3 = elves_summed[:3]
        summed = sum(top_3)
        return summed

puzzle = SolvedPuzzle()
puzzle.solve()