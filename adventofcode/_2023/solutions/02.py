import math
from typing import Dict, List
from adventofcode._templates.puzzle_to_solve import PuzzleToSolve
import re

class Bag:
    """
    A bag of cubes. 
    """
    cubes: Dict[str, int]
    def __init__(self, cubes: Dict[str, int]):
        """
        Set the cubes in the bag.
        
        Args:
            cubes (Dict[str, int]): The cubes in the bag.
        
        Example:
            >>> bag = Bag({"red": 1, "blue": 2})
            >>> bag.cubes
            {"red": 1, "blue": 2}
        """
        self.cubes = cubes
    
    def draw(self, color: str, amount: int):
        """
        Draw a certain amount of cubes from the bag. This means lowering the amount of cubes in the bag.
        If the color is not present, raise a ValueError.
        If the amount of cubes is not present, raise a ValueError.
        
        """
        if color not in self.cubes:
            raise ValueError(f"Color {color} not in {self}, so cannot draw!")
        if self.cubes[color] < amount:
            raise ValueError(f"Cannot draw {amount} {color} cubes from {self}!")
        self.cubes[color] -= amount
    
    def replace(self, color: str, amount: int):
        """
        Replace a certain amount of cubes in the bag. This means increasing the amount of cubes in the bag.
        If the color is not present, raise a ValueError.
        """
        if color not in self.cubes:
            raise ValueError(f"Canot replace color {color} in {self}, since it is not present!")
        self.cubes[color] += amount
    
    def draw_and_replace(self, color: str, amount: int):
        """
        Draw a certain amount of cubes from the bag, and replace it. Raise a ValueError if this is not possible.
        """
        self.draw(color, amount)
        self.replace(color, amount)
    
    def __repr__(self):
        return f"Bag({self.cubes})"

    def power(self) -> int:
        """
        The power of a bag is the product of the amount of cubes in the bag.
        Example:
            >>> bag = Bag({"red": 3, "blue": 4})
            >>> bag.power()
            12
        """
        return math.prod(self.cubes.values())
    

class Grab:
    cubes: Dict[str, int]
    def __init__(self, str_repr: str) -> None:
        """
        Initialze a grab from a string representation.
        Example:
            >>> grab = Grab("3 red, 4 blue")
            >>> grab.cubes
            {"red": 3, "blue": 4}
        """
        str_repr = str_repr.strip()
        regex = r"(\d+) (\w+)"
        if not re.match(regex, str_repr):
            raise ValueError(f"Cannot parse grab {str_repr}!")
        matches = re.findall(regex, str_repr)
        self.cubes = {color: int(amount) for amount, color in matches}
    
    def is_possible_for(self, bag: Bag) -> bool:
        """
        Check if this grab is possible for a certain bag.
        
        Args:
            bag (Bag): The bag to check.
        
        Returns:
            bool: True if the grab is possible for the bag, False otherwise.
            
        Example:
            >>> bag = Bag({"red": 3, "blue": 4})
            >>> grab = Grab("3 red, 4 blue")
            >>> grab.is_possible_for(bag)
            True
            >>> grab = Grab("3 red, 5 blue")
            >>> grab.is_possible_for(bag)
            False
        """
        for color, amount in self.cubes.items():
            try: 
                bag.draw_and_replace(color, amount)
            except ValueError as e:
                print(e)
                return False
        return True

    def __repr__(self):
        return f"Grab({self.cubes})"


class Game:
    """
    A game consists of a number of grabs.
    """
    id: int
    grabs: List[Grab]
    
    def __init__(self, str_repr: str):
        """
        Initialize a game from a string representation.
        
        Args:
            str_repr (str): The string representation of the game.
        
        Example:
            >>> game = Game("Game 1: 3 red, 4 blue; 1 red, 2 green, 6 blue; 2 green")
            >>> game.id
            1
            >>> game.grabs
            [Grab({"red": 3, "blue": 4}), Grab({"red": 1, "green": 2, "blue": 6}), Grab({"green": 2})]
        """
        str_repr = str_repr.strip()
        regex = r"Game (\d+): (.+)"
        if not (match := re.match(regex, str_repr)):
            raise ValueError(f"Cannot parse game {str_repr}!")
        self.id = int(match.group(1))
        self.grabs = [Grab(grab_repr) for grab_repr in match.group(2).split(";")]
    
    
    def is_possible_for(self, bag: Bag) -> bool:
        """Check if this game is possible for a certain bag. The game draws cubes from the bag with replacement.
        The bag must be able to provide the cubes for all grabs in the game.

        Args:
            bag (Bag): The bag to check.

        Returns:
            bool: True if the game is possible for the bag, False otherwise.
        
        Example:
            >>> bag = Bag({"red": 3, "blue": 4})
            >>> game = Game("Game 1: 3 red, 4 blue; 1 red, 2 blue")
            >>> game.is_possible_for(bag)
            True
            >>> bag = Bag({"red": 3, "blue": 2, "green": 2})
            >>> game.is_possible_for(bag)
            False
        """
        for grab in self.grabs:
            if not grab.is_possible_for(bag):
                return False
        return True

    def find_smallest_bag(self) -> Bag:
        """
        Find the smallest bag that can be used to play this game.
        
        Returns:
            Bag: The smallest bag that can be used to play this game.
            
        Example:
            >>> game = Game("Game 1: 3 red, 4 blue; 1 red, 2 blue")
            >>> game.find_smallest_bag()
            Bag({"red": 3, "blue": 4})
        """
        cubes = {}
        for grab in self.grabs:
            for color, amount in grab.cubes.items():
                if color not in cubes:
                    cubes[color] = amount
                else:
                    cubes[color] = max(cubes[color], amount)
        return Bag(cubes)

    def __repr__(self):
        return f"Game({self.id}): {self.grabs}"


class Puzzle2(PuzzleToSolve):
    @property
    def day(self) -> int:
        return 2
    
    @property
    def year(self) -> int:
        return 2023

    @property
    def test_input(self) -> str:
        return """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""

    @property
    def test_answer_a(self):
        return 8

    @property
    def test_answer_b(self):
        return 2286

    def a(self, input_: str):
        bag = Bag({"red": 12, "green": 13, "blue": 14})
        games = [Game(game_repr) for game_repr in input_.splitlines()]
        possible_games = [game for game in games if game.is_possible_for(bag)]
        return sum([game.id for game in possible_games])
        
    def b(self, input_: str):
        games = [Game(game_repr) for game_repr in input_.splitlines()]
        smallest_bags = [game.find_smallest_bag() for game in games]
        return sum([bag.power() for bag in smallest_bags])


puzzle = Puzzle2()
puzzle.solve()
