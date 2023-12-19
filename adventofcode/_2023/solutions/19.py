from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List

import numpy as np
from adventofcode._templates.v20231204.puzzle_to_solve import PuzzleToSolve
import re

class Part:
    x: int
    m: int
    a: int
    s: int
    
    def __init__(self, input_: str):
        """
        
        Example:
        >>> Part('{x=787,m=2655,a=1222,s=2876}')
        Part(x=787, m=2655, a=1222, s=2876)
        """
        regex = r'\{x=(?P<x>\d+),m=(?P<m>\d+),a=(?P<a>\d+),s=(?P<s>\d+)\}'
        match = re.match(regex, input_)
        for attr in ['x', 'm', 'a', 's']:
            setattr(self, attr, int(match.group(attr)))
    
    def ratings(self) -> int:
        return self.x + self.m + self.a + self.s

@dataclass
class Rule:
    condition_attr: str
    condition_operator: str
    condition_value: int
    destination: str
    
    def matches(self, part: Part) -> bool:
        if self.condition_attr is None:
            return True
        if self.condition_operator == '<':
            return getattr(part, self.condition_attr) < self.condition_value
        elif self.condition_operator == '>':
            return getattr(part, self.condition_attr) > self.condition_value
        elif self.condition_operator == '=':
            return getattr(part, self.condition_attr) == self.condition_value
        elif self.condition_operator == "<>":
            return getattr(part, self.condition_attr) != self.condition_value
        else:
            raise Exception(f'Unknown operator {self.condition_operator}')
    
    def invert(self):
        new_attr = self.condition_attr
        if self.condition_operator == '<':
            new_operator = '>'
            new_value = self.condition_value - 1
        elif self.condition_operator == '>':
            new_operator = '<'
            new_value = self.condition_value + 1
        elif self.condition_operator == '=':
            new_operator = '<>'
            new_value = self.condition_value
        elif self.condition_operator == '<>':
            new_operator = '='
            new_value = self.condition_value
        else:
            raise Exception(f'Unknown operator {self.condition_operator}')
        return Rule(new_attr, new_operator, new_value, self.destination)
            

    def find_matched_parts(self) -> Dict[str, List[int]]:
        """
        All possible values of an attribute are 0 - 4000
        Return a dict, with a single element. It maps the attribute to the list of possible values.
        
        Example:
        >>> Rule('m', '<', 100, 'A').find_matched_parts()
        {'m': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, ..., 99]}
        """
        if self.condition_attr is None:
            return {}
        if self.condition_operator == '<':
            return {self.condition_attr: list(range(self.condition_value))}
        elif self.condition_operator == '>':
            return {self.condition_attr: list(range(self.condition_value + 1, 4000))}
        elif self.condition_operator == '=':
            return {self.condition_attr: [self.condition_value]}
        else:
            raise Exception(f'Unknown operator {self.condition_operator}')
    
    def find_unmatched_parts(self) -> Dict[str, List[int]]:
        """
        Invert of find_matched_parts.
        Example:
        >>> Rule('m', '<', 100, 'A').find_unmatched_parts()
        {'m': [100, 101, 102, 103, 104, 105, 106, 107, 108, 109, ..., 3999]}
        """
        return self.invert().find_matched_parts()

class Workflow:
    name: str
    rules: List[Rule]
    
    def __init__(self, input_: str):
        """
        Parse the input.
        
        Example:
        >>> Workflow('px{a<2006:qkq,m>2090:A,rfg}')
        Workflow(name='px', rules=[Rule(condition_attr='a', condition_operator='<', condition_value=2006, destination='qkq'), Rule(condition_attr='m', condition_operator='>', condition_value=2090, destination='A'), Rule(condition_attr='rfg', condition_operator=None, condition_value=None, destination=None)])
        """
        regex = r'(?P<name>\w+){(?P<rules>.*)}'
        match = re.match(regex, input_)
        self.name = match.group('name')
        self.rules = []
        for rule in match.group('rules').split(','):
            if ':' in rule:
                regex = r'(?P<attr>[a-z])(?P<operator>[<>=]+)(?P<value>\d+):(?P<destination>\w+)'
                attr, operator, value, destination = re.match(regex, rule).groups()
                self.rules.append(Rule(attr, operator, int(value), destination))
            else:
                destination = rule
                self.rules.append(Rule(None, None, None, destination))


    def find_unmatched_parts(self) -> Dict[str, List[int]]:
        """
        Find all parts that do not match any rule.
        """
        matched_parts = defaultdict(set)
        for rule in self.rules:
            for attr, values in rule.find_matched_parts().items():
                matched_parts[attr].update(values)
        unmatched_parts = {}
        for attr, values in matched_parts.items():
            unmatched_parts[attr] = set(range(4000)) - values
        return unmatched_parts

    
class System:
    workflows: Dict[str, Workflow]
    parts: List[Part]
    
    def __init__(self, input_: str):
        """
        Create the workflows and parts
        """
        workflows, parts = input_.split('\n\n')
        self.workflows = {}
        for workflow_str in workflows.split('\n'):
            workflow = Workflow(workflow_str)
            self.workflows[workflow.name] = workflow
        self.workflows['A'] = Workflow('A{}')
        self.workflows['R'] = Workflow('R{}')
        self.parts = [Part(part) for part in parts.split('\n')]
    
    def apply(self) -> int:
        """
        Loop over the parts, and apply the rules until the part is accepted or rejected.
        Return the sum of the ratings of the accepted parts.
        """
        accepted_parts = []
        for part in self.parts:
            workflow = self.workflows["in"]
            while workflow.name not in ['R', 'A']:
                for rule in workflow.rules:
                    if rule.matches(part):
                        workflow = self.workflows[rule.destination]
                        break
            if workflow.name == 'A':
                accepted_parts.append(part)
        return sum([part.ratings() for part in accepted_parts])
    
    def find_rules_for_rejected_parts(self) -> List[Rule]:
        """
        Find all rules that lead to a rejected part.
        """
        result = [rule for workflow in self.workflows.values() for rule in workflow.rules if rule.destination == 'R' and rule.condition_attr is not None]
        return result
    
    def find_workflows_for_rejected_parts(self) -> List[Workflow]:
        """
        Find all workflows that lead to a rejected part.
        """
        result = [workflow for workflow in self.workflows.values() if workflow.rules[-1].destination == 'R']
        return result
    
    def find_acceptable_parts(self) -> int:
        """
        Find all parts that are acceptable.
        Doesn't work, because the matrix doesn't fit into memory
        Return the number of acceptable parts.
        """
        part_types = ['x', 'm', 'a', 's']
        # Parts on the dimensions of x, m, a, s
        acceptable_parts = np.ones((4000, 4000, 4000, 4000), dtype=bool)
        for rule in self.find_rules_for_rejected_parts():
            attr, ranges = rule.find_matched_parts().popitem()
            ranges = [range(4000) if attr != p_type else ranges for p_type in part_types]
            acceptable_parts[tuple(ranges)] = False
        for workflow in self.find_workflows_for_rejected_parts():
            unmatched_parts = workflow.find_unmatched_parts()
            ranges = [range(4000) if attr not in part_types else unmatched_parts[attr] for attr in part_types]
            acceptable_parts[tuple(ranges)] = False
        return np.count_nonzero(acceptable_parts)
        


class Puzzle19(PuzzleToSolve):
    @property
    def day(self) -> int:
        return 19
    
    @property
    def year(self) -> int:
        return 2023

    @property
    def test_input(self) -> str:
        return """px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}"""

    @property
    def test_answer_a(self):
        return 19114

    @property
    def test_answer_b(self):
        return 167409079868000

    def parse_input(self, input_: str) -> System:
        return System(input_)

    def a(self, system: System):
        return system.apply()

    def b(self, system: System):
        return system.find_acceptable_parts()


puzzle = Puzzle19()
puzzle.solve()
