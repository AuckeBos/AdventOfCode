from src._2022.puzzle_to_solve import PuzzleToSolve


class Puzzle1(PuzzleToSolve):
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

    """
    Solve a:
    - Split on newlines. One string per Elve
    - Split the string of each Elve. List of strings per Elve
    - Cast each value. List of ints per Elve
    - Sum for each Elve. One int per Elve
    - Take the max Elve
    """

    def a(self, input: str) -> int:
        elves = input.split("\n\n")
        elves_parsed = [elve.split("\n") for elve in elves]
        elves_cast = [[int(i) for i in elve] for elve in elves_parsed]
        elves_summed = [sum(elve) for elve in elves_cast]
        max_elve = max(elves_summed)
        return max_elve

    """
    Solve b:
    - Split on newlines. One string per Elve
    - Split the string of each Elve. List of strings per Elve
    - Cast each value. List of ints per Elve
    - Sum for each Elve. One int per Elve
    - Sort the list of Elves descending: Max Elves first
    - Take the top three Elves
    - Sum the top 3
    """

    def b(self, input: str) -> int:
        elves = input.split("\n\n")
        elves_parsed = [elve.split("\n") for elve in elves]
        elves_cast = [[int(i) for i in elve] for elve in elves_parsed]
        elves_summed = [sum(elve) for elve in elves_cast]
        elves_summed.sort(reverse=True)
        top_3 = elves_summed[:3]
        summed = sum(top_3)
        return summed


puzzle = Puzzle1()
puzzle.solve()
