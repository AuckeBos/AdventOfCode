from puzzle_to_solve import PuzzleToSolve


class Puzzle2(PuzzleToSolve):

    losing_combinations = [
        'A Z',
        'B X',
        'C Y'
    ]

    winning_combinations = [
        'A Y',
        'B Z',
        'C X'
    ]

    draw_combinations = [
        'A X',
        'B Y',
        'C Z'
    ]
    @property
    def day(self) -> int:
        return 2

    @property
    def test_input(self) -> str:
        return """A Y
B X
C Z"""

    @property
    def test_answer_a(self):
        return 15

    @property
    def test_answer_b(self):
        return 12


    def compute_part_1(self, game: str):
        if 'X' in game:
            return 1
        elif 'Y' in game:
            return 2
        elif 'Z' in game:
            return 3
        else:
            raise Exception(f'Cannot compute part 1 of game {game}')

    def compute_part_2(self, game: str):
        if game in self.winning_combinations:
            return 6
        elif game in self.losing_combinations:
            return 0
        elif game in self.draw_combinations:
            return 3
        else:
            raise Exception(f'Cannot compute part 2 of game {game}')

    def compute_score(self, game: str):
        return self.compute_part_1(game) + self.compute_part_2(game)


    def a(self, input: str) -> int:
        games = input.split("\n")
        scores = [self.compute_score(game) for game in games]

        return sum(scores)

    def update_game(self, game:str):
        if 'X' in game:
            list_to_use = self.losing_combinations
        elif 'Y' in game:
            list_to_use = self.draw_combinations
        elif 'Z' in game:
            list_to_use  = self.winning_combinations
        else:
            raise Exception(f'Cannot find the list to update game {game}')
        opponents_choice = game[0]
        updated_game = [x for x in list_to_use if opponents_choice in x][0]
        return updated_game


    def b(self, input: str) -> int:
        games = input.split("\n")
        updated_games = [self.update_game(game) for game in games]
        scores = [self.compute_score(game) for game in updated_games]

        return sum(scores)


puzzle = Puzzle2()
puzzle.solve()
