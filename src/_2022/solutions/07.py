import re
from dataclasses import dataclass, field
from typing import List, Optional, Dict

from src._2022.puzzle_to_solve import PuzzleToSolve


@dataclass
class Node:
    name: str
    parent: 'Node' = None
    children: Dict[str, 'Node'] = field(default_factory=lambda: {})
    size: int = 0

    def parse_input(self, remaining_input: List[str]):
        if not remaining_input:
            return
        item = remaining_input.pop(0)
        if item.startswith('$ cd'):
            new_node = self.parse_cd(item)
        elif item.startswith('$ ls'):
            new_node = self.parse_ls(item)
        elif item.startswith('dir'):
            new_node = self.parse_dir(item)
        else:
            new_node = self.parse_file(item)
        new_node.parse_input(remaining_input)

    def parse_cd(self, line: str):
        name = line[5:]
        if name == '..':
            return self.parent
        else:
            return self.children[name]

    def parse_ls(self, line: str):
        return self

    def parse_dir(self, line: str):
        name = line[4:]
        child = Node(name=name, parent=self)
        self.children[name] = child
        return self

    def parse_file(self, line: str):
        size, name = re.search("(\d+) (.*)", line).groups()
        size = int(size)
        child = Node(name=name, parent=self, size=size)
        self.children[name] = child
        return self

    def get_children_of_at_most_size(self, size: int):
        result = []
        for child in self.children.values():
            result.extend(child.get_children_of_at_most_size(size))
        if self.size_sum <= size and len(self.children) > 0:
            result.append(self)
        return result

    @property
    def size_sum(self):
        return self.size + sum([x.size_sum for x in self.children.values()])

    def get_children_dirs(self):
        if self.children:
            result = [self]
            for child in self.children.values():
                result.extend(child.get_children_dirs())
            return result
        return []


class Puzzle7(PuzzleToSolve):
    @property
    def day(self) -> int:
        return 7

    @property
    def test_input(self) -> str:
        return """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k"""

    @property
    def test_answer_a(self):
        return 95437

    @property
    def test_answer_b(self):
        return 24933642

    def a(self, input: str):
        items = input.split('\n')
        first = items.pop(0)
        assert first == '$ cd /'
        root = Node(name='/')
        root.parse_input(items)
        result = root.get_children_of_at_most_size(100000)
        summed = sum([x.size_sum for x in result])
        return summed

    def b(self, input: str):
        items = input.split('\n')
        first = items.pop(0)
        assert first == '$ cd /'
        root = Node(name='/')
        root.parse_input(items)
        current_size = root.size_sum
        current_free = 70000000 - current_size
        to_free = 30000000 - current_free
        options = [x for x in root.get_children_dirs() if x.size_sum >= to_free]
        sorted_options = sorted(options, key=lambda x: x.size_sum)
        item_to_delete = sorted_options[0]
        return item_to_delete.size_sum


puzzle = Puzzle7()
puzzle.solve()
