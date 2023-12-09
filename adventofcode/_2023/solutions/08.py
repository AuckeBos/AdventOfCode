from adventofcode._templates.v20231204.puzzle_to_solve import PuzzleToSolve
from typing import Dict, List
import re
from collections import defaultdict
import sys
import math
class Network:
    """
    Network of nodes
    
    Attributes:
        instructions: str
            List of LR instructions
        nodes: Dict[str, Dict[str, str]]
            Dictionary of nodes, with keys being the node names, and values being a dictionary of instructions and the next node
        start_nodes = List[str]
            List of start nodes. Is [AAA] for the normal network, and every node that ends with A for the ghost network
    """
    
    instructions: str
    nodes: Dict[str, Dict[str, str]]
    start_nodes = List[str]
    
    def __init__(self, instructions: str, nodes: Dict[str, Dict[str, str]], is_ghost: bool = False):
        """
        Set attributes and define start nodes
        """
        self.instructions = instructions
        self.nodes = nodes
        if is_ghost:
            self.start_nodes = [n for n in self.nodes.keys() if n.endswith("A")]
        else:
            self.start_nodes = ["AAA"]
    
    def set_is_ghost(self) -> "Network":
        """
        Return a new network, with the ghost nodes
        """
        return Network(self.instructions, self.nodes, True)
    
    def run(self):
        """
        For each start node, run until the node ends with Z.
        Return the LCM of the number of steps needed for each start node
        """
        needed_steps = []
        for node in self.start_nodes:
            i = 0
            while not node.endswith("Z"):
                node = self.nodes[node][self.instructions[i % len(self.instructions)]]
                i += 1
            needed_steps.append(i)
        return math.lcm(*needed_steps)
    


class Puzzle8(PuzzleToSolve):
    @property
    def day(self) -> int:
        return 8
    
    @property
    def year(self) -> int:
        return 2023

    @property
    def test_input(self) -> str:
        return """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)"""

    @property
    def test_input_alternative(self) -> str:
        return """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""

    @property
    def test_answer_a(self):
        return 6

    @property
    def test_answer_b(self):
        return 6

    def parse_input(self, input_: str) -> Network:
        instructions, nodes = input_.split("\n\n")
        regex = r"(\w+) = \((\w+), (\w+)\)"
        nodes = {
            g[0]: {"L": g[1], "R": g[2]} for g in re.findall(regex, nodes)
        }
        return Network(instructions, nodes)

    def a(self, network: Network):
        """
        Run the normal network, ie find the number of steps needed to go from AAA to ZZZ
        """
        return network.run()

    def b(self, network: Network):
        """
        Run the ghost network, ie find the number of steps needed to go from every node that ends with A to a node that ends with Z
        """
        return network.set_is_ghost().run()

puzzle = Puzzle8()
puzzle.solve()
