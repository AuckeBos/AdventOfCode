from adventofcode._templates.v20231204.puzzle_to_solve import PuzzleToSolve
from collections import defaultdict
from typing import List
class Hand:
    """
    A Hand of cards. Can be compared to other hands.
    
    Attributes:
        cards (str): A string of 5 cards
        bid (int): The bid for this hand
        HAND_COUNTS_ORDERING (List[str]): The ordering of hand counts. First index is best hand
        CARD_ORDERING (List[str]): The ordering of cards
        SPECIAL_CARD_ORDERING (List[str]): The ordering of cards when jokers are used (ie J is Joker instead of Jack)
        use_jokers (bool): Whether to use jokers or not. Can be set with set_use_jokers
    """
    cards: str
    bid: int
    
    HAND_COUNTS_ORDERING = [
        "5", # Five of a kind
        "41", # Four of a kind
        "32", # Full house
        "311", # Three of a kind 
        "221", # Two pairs
        "2111", # One pair
        "11111", # High card
    ]
    
    CARD_ORDERING = [
        "A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"
    ]
    
    SPECIAL_CARD_ORDERING = [
        "A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"
    ]
    
    use_jokers: bool = False
    
    def __init__(self, cards: str, bid: int):
        self.cards = cards
        self.bid = bid
    
    def set_use_jokers(self, use_jokers: bool):
        self.use_jokers = use_jokers
        return self
    
    @property
    def counts(self):
        """
        Count the number of times each card occurs.
        If jokers are used, add them to the most common card.
        
        Returns:
            str: A string of the counts of each card, sorted by most common.
            
        Example: "311" means three of one card, one of another, and one of another
        """
        if self.cards == "JJJJJ":
            return "5"
        d = defaultdict(int)
        jokers = 0
        for c in self.cards:
            if self.use_jokers and c == "J":
                jokers += 1
            else:
                d[c] += 1
        # Sort on descending values
        sorted_values = sorted(d.values(), reverse=True)
        # If use jokers, add them to the most common card
        if jokers > 0:
            sorted_values[0] += jokers
        # Sanity check
        if sum(sorted_values) != 5:
            raise ValueError(f"Invalid hand: {self.cards}")
        return ''.join([str(v) for v in sorted_values])
    
    def __lt__(self, other):
        """
        Check if the current card is worse than the other card.
        If the counts are different, use the HAND_COUNTS_ORDERING to determine which is better.
        If the counts are the same, use the CARD_ORDERING to determine which is better.
        """
        if self.counts != other.counts:
            return self.HAND_COUNTS_ORDERING.index(self.counts) > self.HAND_COUNTS_ORDERING.index(other.counts)
        
        ordering = self.CARD_ORDERING if not self.use_jokers else self.SPECIAL_CARD_ORDERING
        for c1, c2 in zip(self.cards, other.cards):
            if c1 != c2:
                return ordering.index(c1) > ordering.index(c2)
        
        raise ValueError(f"Hands are equal: {self.cards} and {other.cards}")

    def __repr__(self):
        return self.cards


class Puzzle7(PuzzleToSolve):
    @property
    def day(self) -> int:
        return 7
    
    @property
    def year(self) -> int:
        return 2023

    @property
    def test_input(self) -> str:
        return """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""

    @property
    def test_answer_a(self):
        return 6440

    @property
    def test_answer_b(self):
        return 5905

    def parse_input(self, input_: str):
        lines = input_.splitlines()
        hands = [Hand(cards, int(bid)) for cards, bid in [line.split() for line in lines]]
        return hands


    def a(self, hands: List[Hand]):
        """
        Sort the hands, then compute the score.
        """
        hands = sorted(hands)
        score = 0
        for i, hand in enumerate(hands):
            score += (i + 1) * hand.bid
        return score        

    def b(self, hands: List[Hand]):
        """
        Sort the hands, use use_jokers, then compute the score.
        """
        hands = [h.set_use_jokers(True) for h in hands]
        hands = sorted(hands)
        score = 0
        for i, hand in enumerate(hands):
            score += (i + 1) * hand.bid
        return score


puzzle = Puzzle7()
puzzle.solve()
