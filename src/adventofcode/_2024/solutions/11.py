from adventofcode._templates.v20231204.puzzle_to_solve import PuzzleToSolve


class Puzzle11(PuzzleToSolve):
    @property
    def day(self) -> int:
        return 11

    @property
    def year(self) -> int:
        return 2024

    @property
    def test_input(self) -> str:
        return "125 17"

    @property
    def test_answer_a(self):
        return 55312

    @property
    def test_answer_b(self):
        return 65601038650482

    def split_stone(self, stone: str, n: int) -> int:
        if n == 0:
            return 1
        if (stone, n) in self.history:
            return self.history[(stone, n)]
        if stone == "0":
            stones = ["1"]
        elif len(stone) % 2 == 0:
            stones = [
                str(int(stone[: len(stone) // 2])),
                str(int(stone[len(stone) // 2 :])),
            ]
        else:
            stones = [str(int(stone) * 2024)]
        result = sum(self.split_stone(stone, n - 1) for stone in stones)
        self.history[(stone, n)] = result
        return result

    def blink(self, stones: list[str], n: int) -> list[str]:
        self.history: dict[tuple[str, int]] = {}
        return sum(self.split_stone(stone, n) for stone in stones)

    def parse_input(self, input_: str) -> list[str]:
        return input_.split(" ")

    def a(self, stones: list[str]) -> int:
        return self.blink(stones, 25)

    def b(self, stones: list[str]) -> int:
        return self.blink(stones, 75)


puzzle = Puzzle11()
puzzle.solve()
