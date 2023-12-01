from adventofcode._2023.puzzle_to_solve import PuzzleToSolve
from word2number import w2n

class Puzzle1(PuzzleToSolve):
    @property
    def day(self) -> int:
        return 1

    @property
    def test_input(self) -> str:
        return """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet"""

    @property
    def test_input_alternative(self) -> str:
        return """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""
    @property
    def test_answer_a(self):
        return 142

    @property
    def test_answer_b(self):
        return 281

    def a(self, input_: str) -> int:
        """
        - Split the input on lines
        - For each line, find the digits
        - Combine the first and last digit into one number
        - Sum all numbers
        """
        lines = input_.splitlines()
        line_digits = [[c for c in line if c.isdigit()] for line in lines]
        combined_items = [int(line[0] + line[-1]) for line in line_digits]
        result = sum(combined_items)
        return result

    def b(self, input_: str):
        """
        - ns is the ns for which we want to find ngrams
        - For each line, for each n, find all the ngrams
        - If an ngram is a digit or the word representation of a digit, add it to the list of digits
        - For each line, sort the digits on the index on which they were found in the line
        - For each line, take the first and last digit, combine them into one number
        - Sum all numbers
        """
        ns = range(1, 6)
        lines = input_.splitlines()
        line_digits = []
        for line in lines:
            digits = []
            for n in ns:
                for i in range(len(line)-n+1):
                    ngram = line[i:i+n]
                    try:
                        if ngram.isdigit():
                            digit = int(ngram)
                            digits.append((digit, i))
                        else:
                            digit = w2n.word_to_num(ngram)
                            digits.append((digit, i))
                    except ValueError:
                        pass
            line_digits.append(digits)
        
        line_digits = [sorted(digits, key=lambda x: x[1]) for digits in line_digits]
        combined_items = [int(str(digits[0][0]) + str(digits[-1][0])) for digits in line_digits]
        result = sum(combined_items)
        return result

puzzle = Puzzle1()
puzzle.solve()
