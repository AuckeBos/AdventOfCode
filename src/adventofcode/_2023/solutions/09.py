from typing import List
from adventofcode._templates.v20231204.puzzle_to_solve import PuzzleToSolve




class Puzzle9(PuzzleToSolve):
    @property
    def day(self) -> int:
        return 9
    
    @property
    def year(self) -> int:
        return 2023

    @property
    def test_input(self) -> str:
        return """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""

    @property
    def test_answer_a(self):
        return 114

    @property
    def test_answer_b(self):
        return 2

    def parse_input(self, input_: str):
        lines = input_.split("\n")
        return [list(map(int, line.split())) for line in lines]

    def a(self, input_: List[List[int]]):
        """
        - Loop over the history of each sensor
        - Compute the diffs between each value, and append to the diffs
        - Repeat, but use the last diffs as value. Continue until all diffs are 0
        - Sum the last value of each diff, add to predictions
        - Return sum of predictions
        
        """
        predictions = []
        for sensor_history in input_:
            diffs: List[List[int]] = [sensor_history]
            while not (diffs[-1] == [0] * len(diffs[-1])):
                diffs.append([diffs[-1][i] - diffs[-1][i - 1] for i in range(1, len(diffs[-1]))])
            predictions.append(sum([diff[-1] for diff in diffs]))
        return sum(predictions)
            
            

    def b(self, input_: List[List[int]]):
        """
        - Loop over the history of each sensor
        - Compute the diffs between each value, and append to the diffs
        - Repeat, but use the last diffs as value. Continue until all diffs are 0
        - Loop over the diffs from the (end - 1) to the beginning
        - Start with prediction=0, subtract the prediction from the first value of the current diff, set it as the new prediction
        - Return sum of predictions
        """
        predictions = []
        for sensor_history in input_:
            diffs: List[List[int]] = [sensor_history]
            while not (diffs[-1] == [0] * len(diffs[-1])):
                diffs.append([diffs[-1][i] - diffs[-1][i - 1] for i in range(1, len(diffs[-1]))])
            prediction = 0
            for diff in diffs[-2::-1]:
                prediction = diff[0] - prediction
            predictions.append(prediction)
        return sum(predictions)        


puzzle = Puzzle9()
puzzle.solve()
