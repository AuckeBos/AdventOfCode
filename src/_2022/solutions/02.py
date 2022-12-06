from src._2022.puzzle_to_solve import PuzzleToSolve


class Puzzle2(PuzzleToSolve):

    """
    List of games that will result in a loss
    """
    losing_combinations = [
        'A Z',
        'B X',
        'C Y'
    ]
    """
    List of games that will result in a winn
    """
    winning_combinations = [
        'A Y',
        'B Z',
        'C X'
    ]
    """
    List of games that will result in a draw
    """
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


    """
    Compute part 1 of the score of a game, based on own choice
    """
    def compute_part_1(self, game: str):
        if 'X' in game:
            return 1
        elif 'Y' in game:
            return 2
        elif 'Z' in game:
            return 3
        else:
            raise Exception(f'Cannot compute part 1 of game {game}')
    """
    Compute part 2 of the score of a game, based on result of the game
    """
    def compute_part_2(self, game: str):
        if game in self.winning_combinations:
            return 6
        elif game in self.losing_combinations:
            return 0
        elif game in self.draw_combinations:
            return 3
        else:
            raise Exception(f'Cannot compute part 2 of game {game}')

    """
    Compute the score of a game, by summing the first and the second part
    """
    def compute_score(self, game: str):
        return self.compute_part_1(game) + self.compute_part_2(game)


    """
    Solve a:
    - Parse: One string per game
    - Compute the score for each game
    - Sum the result
    """
    def a(self, input: str) -> int:
        games = input.split("\n")
        scores = [self.compute_score(game) for game in games]

        return sum(scores)

    """
    Update the game, to solve b:
    - Select one of the three combinations list, based on the second part of the game
    - For the selected list, select the game that belongs to the choice that the opponent made
    - Now the result is the game how it should be played, in the format of a). Hence we can solve using the impl of a)
    """
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

    """
    Solve b:
    - Update each game, such that it is in the same format as the games in part a)
    - Solve equal to part a
    """
    def b(self, input: str) -> int:
        games = input.split("\n")
        updated_games = [self.update_game(game) for game in games]
        scores = [self.compute_score(game) for game in updated_games]

        return sum(scores)


puzzle = Puzzle2()
puzzle.solve()
