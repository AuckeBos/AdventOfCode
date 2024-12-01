from abc import abstractmethod
from collections import defaultdict
from adventofcode._templates.v20231204.puzzle_to_solve import PuzzleToSolve
import re
from typing import Dict, List, Tuple
import math

class Module:
    type_: str
    name: str
    destinations: List[str]
    
    def __init__(self, type_: str, name: str, destinations: List[str]):
        self.type_ = type_
        self.name = name
        self.destinations = destinations
        
    def add_source(self, source: str):
        """
        Only used for conjunctions
        """
        pass
        
    @abstractmethod
    def receive_pulse(self, source: str, pulse: bool, button_press_count: int = None) -> List[Tuple[str, bool, str]]:
        """
        Receive a pulse. Update the state if needed.
        
        Args:
            source: The source of the pulse.
            pulse: The pulse to receive. False = low, True = high
        
        Returns:
            A list of tuples containing the destination and the pulse to send to that destination.
        """
        pass

        
    def __repr__(self):
        return f"{self.type_}{self.name} -> {self.destinations}"
    
class Broadcaster(Module):
    type_: str = ""
    
    def __init__(self, type_: str, name: str, destinations: List[str]):
        super().__init__(type_, name, destinations)
        self.name = "broadcaster"
    
    def receive_pulse(self, source: str, pulse: bool, button_press_count: int = None) -> List[Tuple[str, bool, str]]:
        return [(self.name, pulse, destination) for destination in self.destinations]

    def __hash__(self):
        return hash((self.name))

class Conjunction(Module):
    type_: str = "&"
    last_pulses: Dict[str, bool]
    # Keep track of the button press count, whenever a high pulse is received from a source
    memory: Dict[str, List[int]]
    
    def __init__(self, type_: str, name: str, destinations: List[str]):
        super().__init__(type_, name, destinations)
        self.last_pulses = {}
        self.memory = defaultdict(list)
    
    def add_source(self, source: str):
        self.last_pulses[source] = False
    
    def receive_pulse(self, source: str, pulse: bool, button_press_count: int = None) -> List[Tuple[str, bool]]:
        if source not in self.last_pulses:
            raise ValueError(f"Source {source} not in last_pulses")
        if pulse:
            self.memory[source].append(button_press_count)
        self.last_pulses[source] = pulse
        if list(self.last_pulses.values()) == [True] * len(self.last_pulses):
            return [(self.name, False, destination) for destination in self.destinations]
        else:
            return [(self.name, True, destination) for destination in self.destinations]
    
    def __hash__(self):
        return hash((self.name, tuple([(k, v) for k, v in self.last_pulses.items()])))

class FlipFlow(Module):
    type_: str = "%"
    state: bool
    
    def __init__(self, type_: str, name: str, destinations: List[str]):
        super().__init__(type_, name, destinations)
        self.state = False
    
    def receive_pulse(self, source: str, pulse: bool, button_press_count: int = None) -> List[Tuple[str, bool, str]]:
        if pulse:
            return []
        else:
            self.state = not self.state
            if self.state: # was off
                return [(self.name, True, destination) for destination in self.destinations]
            else:
                return [(self.name, False, destination) for destination in self.destinations]

    def __hash__(self):
        return hash((self.name, self.state))
class Button(Module):
    type_: str = ""
    
    def __init__(self, type_: str, name: str, destinations: List[str]):
        super().__init__(type_, name, destinations)
        self.name = "button"
    
    def receive_pulse(self, source: str, pulse: bool, button_press_count: int = None) -> List[Tuple[str, bool, str]]:
        return [("button", False, "broadcaster")]

    def __hash__(self):
        return hash((self.name))

class Output(Module):
    type_: str = ""
    
    def __init__(self, type_: str, name: str, destinations: List[str]):
        super().__init__(type_, name, destinations)
        self.name = "output"
    
    def receive_pulse(self, source: str, pulse: bool, button_press_count: int = None) -> List[Tuple[str, bool, str]]:
        return []

    def __hash__(self):
        return hash((self.name))

class Puzzle20(PuzzleToSolve):
    
    MODULE_CLASSES = {
        "": Broadcaster,
        "&": Conjunction,
        "%": FlipFlow,
    }
    @property
    def day(self) -> int:
        return 20
    
    @property
    def year(self) -> int:
        return 2023

    @property
    def test_input(self) -> str:
        return r"""broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a"""
        return r"""broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output"""

    @property
    def test_answer_a(self):
        return 32000000
        return 11687500

    @property
    def test_answer_b(self):
        return -1


    def push_button(self, modules: Dict[str, Module], amount: int) -> List[Tuple[str, bool, str]]:
        low_pushes, high_pushes = 0, 0
        for _ in range(amount):
            modules, low, high = self.push_button_once(modules)
            low_pushes += low
            high_pushes += high
        return low_pushes * high_pushes
    
    def push_button_once(self, modules: Dict[str, Module], button_press_count: int = None) -> Tuple[Dict[str, Module], int, int]:
        """
        Push the buttons once, and continue until all pulses have been sent.
        Return the new modules, and the amount of False and True pulses sent.
        """
        low_pulses, high_pulses = 0, 0
        stack = [("", False, "button")]
        while len(stack) > 0:
            source, pulse, destination = stack.pop(0)
            if destination != "button":
                if pulse:
                    high_pulses += 1
                else:
                    low_pulses += 1
            if destination in modules:
                new_pulses = modules[destination].receive_pulse(source, pulse, button_press_count)
                stack.extend(new_pulses)
        return modules, low_pulses, high_pulses

    def parse_input(self, input_: str) -> Dict[str, Module]:
        lines = input_.splitlines()
        regex = r"([%&]{0,1})([a-z0-9]+) -> (.+)"
        lines = [re.match(regex, line).groups() for line in lines]
        lines = [(line[0], line[1], line[2].split(", ")) for line in lines]
        modules = {line[1]: self.MODULE_CLASSES[line[0]](*line) for line in lines}
        modules["button"] = Button("", "button", ["broadcaster"])
        modules["output"] = Output("", "output", [])
        for module in modules.values():
            for destination in module.destinations:
                if destination in modules:
                    modules[destination].add_source(module.name)
        return modules

    def a(self, modules: Dict[str, Module]):
        return self.push_button(modules, 1000)
        

    def b(self, modules: Dict[str, Module]):
        modules_with_rx_as_destination = [module for module in modules.values() if "rx" in module.destinations]
        # Test B, no answer
        if not len(modules_with_rx_as_destination):
            return -1
        # The single module with rx as destination
        module_with_rx_as_destination = modules_with_rx_as_destination[0]
        # Done if the module with rx has a memory of the same size as the last pulses. In this case, all inputs have been received at least once
        button_press_count = 1
        while not len(module_with_rx_as_destination.memory) == len(module_with_rx_as_destination.last_pulses):
            self.push_button_once(modules, button_press_count)
            button_press_count += 1
        # Compute the LCM of all the memory values of the module. For this value (or multiples of this value), the module will receive all inputs as True, hence rx will be True
        all_memory = [v for memory in module_with_rx_as_destination.memory.values() for v in memory]
        value = math.lcm(*all_memory)
        return value
    


puzzle = Puzzle20()
puzzle.solve()
