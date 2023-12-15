from typing import List, Tuple
from adventofcode._templates.v20231204.puzzle_to_solve import PuzzleToSolve

def hash_(lens: str) -> int:
    """
    Apply the HASH algorithm to a lens.
    """
    sum = 0
    for c in lens:
        sum = ((sum + ord(c)) * 17) % 256
    return sum

class Box:
    """
    A box has an ordered list of lenses.
    Lenses can be upserted or removed.
    """
    lenses: List[Tuple[str, int]]
    
    def __init__(self):
        self.lenses = []
    
    def has_lens(self, lens: str) -> bool:
        return lens in [l for l, _ in self.lenses]

    def delete_lens(self, lens: str):
        self.lenses = [(l,v) for l,v in self.lenses if l != lens]
    
    def upsert_lens(self, lens: str, value: int):
        for i, (l, _) in enumerate(self.lenses):
            if l == lens:
                self.lenses[i] = (lens, value)
                return
        self.lenses.append((lens, value))

class Room:
    boxes: List[Box]
    
    def __init__(self):
        """
        Create 256 boxes on init.
        """
        self.boxes = [Box() for i in range(256)]
    
    def apply_hashmap(self, input: List[str]) -> int:
        """
        Parse each step, and update the boxes accordingly.
        
        Return the focussing power.
        """
        for step in input:
            self.apply_step(step)
        return self.compute_focussing_power()
    
    def compute_focussing_power(self) -> int:
        """
        Compute the focussing power of the room.
        """
        result = 0
        for box_index, box in enumerate(self.boxes):
            for lens_index, (lens, value) in enumerate(box.lenses):
                result += (box_index + 1) * (lens_index + 1) * value
        return result
    
    def delete_lens(self, lens: str):
        """
        Remove the lens from the box it is in.
        """
        self.boxes[hash_(lens)].delete_lens(lens)

    def upsert_lens(self, lens: str, value: int):
        """
        Upsert the lens to the box it belongs to.
        """
        self.boxes[hash_(lens)].upsert_lens(lens, value)
        
    
    def apply_step(self, step: str):
        """
        Apply a step: Remove the lens, or upsert it.
        """
        if step[-1] == "-":
            self.delete_lens(step[:-1])
        else:
            lens, value = step.split("=")
            self.upsert_lens(lens, int(value))


class Puzzle15(PuzzleToSolve):
    @property
    def day(self) -> int:
        return 15
    
    @property
    def year(self) -> int:
        return 2023

    @property
    def test_input(self) -> str:
        return "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"

    @property
    def test_answer_a(self):
        return 1320

    @property
    def test_answer_b(self):
        return 145

    def parse_input(self, input_: str) -> List[str]:
        return input_.split(",")        

    def a(self, input_: List[str]) -> int:
        """
        Sum the hash of each lens.
        """
        return sum([hash_(lens) for lens in input_])

    def b(self, input_: List[str]) -> int:
        """
        Apply the hashmap to the room, return the focussing power.
        """
        return Room().apply_hashmap(input_)


puzzle = Puzzle15()
puzzle.solve()
