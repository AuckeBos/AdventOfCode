from src._2022.puzzle_to_solve import PuzzleToSolve


class Puzzle6(PuzzleToSolve):
    @property
    def day(cls) -> int:
        return 6

    @property
    def test_input(self) -> str:
        return "mjqjpqmgbljsphdztnvjfqwrcgsmlb"

    @property
    def test_answer_a(self):
        return 7

    @property
    def test_answer_b(self):
        return 19

    def detect_marker(self, input: str, marker_size: int):
        """
        Detect the marker in the input. The marker is found when marker_size distinct chars are found in a row; the
        index of the last char of the marker is returned.
        """
        # Hopping window of len marker_size and step 1
        windows = [input[i:i + marker_size] for i in range(len(input) - marker_size - 1)]
        for i, window in enumerate(windows):
            if len(set(window)) == marker_size:
                return i + marker_size
        raise Exception("No marker found!")

    def a(self, input_: str):
        """
        Solve a) by detecting the first marker of length 4
        """
        return self.detect_marker(input_, 4)

    def b(self, input_: str):
        """
        Solve b) by detecting the first marker of length 14
        """
        return self.detect_marker(input_, 14)


puzzle = Puzzle6()
puzzle.solve()
