import functools
from collections import defaultdict

from adventofcode._templates.v20231204.puzzle_to_solve import PuzzleToSolve


class Puzzle5(PuzzleToSolve):
    """
    Attributes:
        ltr (dict[int, list[int]]): A dictionary mapping a number to the numbers that cannot come before it.
        rtl (dict[int, list[int]]): A dictionary mapping a number to the numbers that cannot come after it.
    """

    ltr: dict[int, list[int]]
    rtl: dict[int, list[int]]

    @property
    def day(self) -> int:
        return 5

    @property
    def year(self) -> int:
        return 2024

    @property
    def test_input(self) -> str:
        return """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""

    @property
    def test_answer_a(self):
        return 143

    @property
    def test_answer_b(self):
        return 123

    def parse_input(self, input_: str) -> list[list[int]]:
        rules, pages_str = input_.split("\n\n")
        ltr, rtl = defaultdict(lambda: []), defaultdict(lambda: [])
        for rule in rules.split("\n"):
            l, r = map(int, rule.split("|"))
            ltr[l].append(r)
            rtl[r].append(l)
        pages = [list(map(int, page.split(","))) for page in pages_str.split("\n")]
        self.ltr, self.rtl = ltr, rtl
        return pages

    def is_correct(self, page: list[int]) -> bool:
        """
        Check if a page is correctly ordered.

        Loop over the numbers. For each, check if the other numbers in the page are
        in the correct position, relative to the current number.
        """
        return all(
            [
                *[
                    (r not in page) or page.index(num) < page.index(r)
                    for num in page
                    for r in self.ltr[num]
                ],
                *[
                    (l not in page) or page.index(l) < page.index(num)
                    for num in page
                    for l in self.rtl[num]
                ],
            ]
        )

    def compare(self, l: int, r: int) -> int:
        """Compare two numbers, according to the rules."""
        if l in self.ltr and r in self.ltr[l]:
            return -1
        if r in self.ltr and l in self.ltr[r]:
            return 1
        return 0

    def fix(self, page: list[int]) -> list[int]:
        """Fix a page by sorting it according to the rules."""
        return sorted(page, key=functools.cmp_to_key(self.compare))

    def a(self, pages: list[list[int]]):
        """Sum the middle number of all correct pages."""
        return sum([page[len(page) // 2] for page in pages if self.is_correct(page)])

    def b(self, pages: list[list[int]]):
        """Sum the middle number of all fixed incorrect pages."""
        return sum(
            [
                self.fix(page)[len(page) // 2]
                for page in pages
                if not self.is_correct(page)
            ]
        )


puzzle = Puzzle5()
puzzle.solve()
