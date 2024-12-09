from adventofcode._templates.v20231204.puzzle_to_solve import PuzzleToSolve


class Puzzle9(PuzzleToSolve):
    @property
    def day(self) -> int:
        return 9

    @property
    def year(self) -> int:
        return 2024

    @property
    def test_input(self) -> str:
        return "2333133121414131402"

    @property
    def test_answer_a(self):
        return 1928

    @property
    def test_answer_b(self):
        return 2858

    def parse_input(self, input_: str) -> list[int | None]:
        blocks = []
        for i, value in enumerate(input_):
            to_add = i // 2 if i % 2 == 0 else None
            blocks.extend([to_add] * int(value))
        return blocks

    def a(self, blocks: list[int | None]) -> int:
        r = len(blocks) - 1
        l = 0
        while l < r:
            if blocks[l] is not None:
                l += 1
                continue
            blocks[l] = blocks[r]
            blocks[r] = None
            while blocks[r] is None:
                r -= 1
        return sum([i * value for i, value in enumerate(blocks) if value is not None])

    def b(self, blocks: list[int | None]) -> int:
        r = len(blocks) - 1
        while r > 0:
            print(f"{len(blocks) - r}/{len(blocks)}", end="\r")
            if blocks[r] is None:
                r -= 1
                continue
            r_end = r
            r_start = r
            while blocks[r_start] == blocks[r_end]:
                r_start -= 1
            to_find_size = r_end - r_start
            r_start += 1

            l = 0
            while l < r_start:
                if blocks[l] is not None:
                    l += 1
                    continue
                l_start = l
                l_end = l
                while blocks[l_end] == blocks[l_start]:
                    l_end += 1
                found_size = l_end - l_start
                if found_size >= to_find_size:
                    blocks[l_start : l_start + to_find_size] = blocks[
                        r_start : r_end + 1
                    ]
                    blocks[r_start : r_end + 1] = [None] * to_find_size
                    break
                l = l_end + 1
            r = r_start - 1
        return sum([i * value for i, value in enumerate(blocks) if value is not None])


puzzle = Puzzle9()
puzzle.solve()
